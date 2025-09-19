from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Tuple, Callable, Iterable, Optional
import operator

Val = int
Assignment = Dict[str, Val]

@dataclass
class CSP:
    domains: Dict[str, List[Val]]
    constraints: List["Constraint"]

@dataclass
class Constraint:
    scope: Tuple[str, ...]
    pred: Callable[[Assignment], bool]
    pretty: str

    def get_description(self):
        return self.pretty

# ---------- Constraint builders ----------
def c_alldiff(vars: List[str]) -> Constraint:
    def pred(a: Assignment) -> bool:
        vals = [a[v] for v in vars if v in a]
        return len(vals) == len(set(vals))
    return Constraint(tuple(vars), pred, f"alldiff({','.join(vars)})")

def c_bin(op: Callable[[int,int], bool], x: str, y: str, opname: str) -> Constraint:
    def pred(a: Assignment) -> bool:
        if x in a and y in a:
            return op(a[x], a[y])
        return True
    return Constraint((x,y), pred, f"{opname}({x},{y})")

def c_in(x: str, allowed: List[int]) -> Constraint:
    def pred(a: Assignment) -> bool:
        return (x not in a) or (a[x] in allowed)
    return Constraint((x,), pred, f"in({x},{allowed})")

def c_sum(vars: List[str], opstr: str, k: int) -> Constraint:
    opmap = {"==": operator.eq, "!=": operator.ne, "<=": operator.le,
             "<": operator.lt, ">=": operator.ge, ">": operator.gt}
    if opstr not in opmap: raise ValueError(f"bad sum op {opstr}")
    opf = opmap[opstr]
    def pred(a: Assignment) -> bool:
        # Accept partial assignments; only check when fully assigned
        if not all(v in a for v in vars):
            return True
        return opf(sum(a[v] for v in vars), k)
    return Constraint(tuple(vars), pred, f"sum({vars}) {opstr} {k}")

def c_table(vars: List[str], allowed: List[Tuple[int, ...]]) -> Constraint:
    allowed_set = set(tuple(t) for t in allowed)
    def pred(a: Assignment) -> bool:
        if all(v in a for v in vars):
            tup = tuple(a[v] for v in vars)
            return tup in allowed_set
        return True
    return Constraint(tuple(vars), pred, f"table({vars}) allowed {allowed}")

def c_add10(x: str, y: str, cin: str, z: str, cout: str) -> Constraint:
    """Digit-wise base-10 addition: x + y + cin = 10*cout + z, where cin, cout in {0,1} and x,y,z in 0..9.
       Partial assignments are allowed; we only enforce when all involved vars are assigned.
    """
    scope = (x, y, cin, z, cout)
    def pred(a: Assignment) -> bool:
        if all(v in a for v in scope):
            return (a[x] + a[y] + a[cin]) == 10 * a[cout] + a[z]
        return True
    return Constraint(scope, pred, f"add10({x},{y},{cin}->{z},{cout})")

# ---------- CSPSolver with Heuristics ----------
class CSPSolver:
    def __init__(self, vars: List[str], domains: Dict[str, List[Val]], constraints: List[Constraint]):
        self.vars = vars
        self.domains = domains
        self.constraints = constraints
        self.cons_by_var: Dict[str, List[Constraint]] = {v: [] for v in vars}
        for c in constraints:
            for v in c.scope:
                if v in self.cons_by_var:
                    self.cons_by_var[v].append(c)
        self.assignment: Assignment = {}
        self.backtracks = 0

    def solve_backtracking(self, heuristic: str = 'None') -> Tuple[bool, Optional[Assignment]]:
        self.backtracks = 0
        self.heuristic = heuristic
        self.domains = {v: list(ds) for v, ds in self.domains.items()} # Use a fresh copy
        solution = next(self._backtrack(), None)
        return solution is not None, solution

    def _consistent_with_local(self, v: str, a: Assignment) -> bool:
        for c in self.cons_by_var[v]:
            if not c.pred(a):
                return False
        return True

    def _select_unassigned_variable(self):
        """Variable ordering heuristic (MRV)."""
        unassigned_vars = [v for v in self.vars if v not in self.assignment]
        if self.heuristic == 'MRV':
            return min(unassigned_vars, key=lambda v: len(self.domains[v]))
        else:
            # Default to first unassigned variable in a fixed order
            for v in self.vars:
                if v not in self.assignment:
                    return v

    def _get_ordered_values(self, var):
        """Value ordering heuristic (LCV)."""
        if self.heuristic == 'LCV':
            # Count the number of domain reductions for each value
            # and sort by least constraining
            value_counts = []
            for val in self.domains[var]:
                count = 0
                self.assignment[var] = val
                for neighbor_cons in self.cons_by_var[var]:
                    for neighbor in neighbor_cons.scope:
                        if neighbor not in self.assignment:
                            # Prune neighbors' domains and count reductions
                            for neighbor_val in self.domains[neighbor]:
                                temp_assignment = self.assignment.copy()
                                temp_assignment[neighbor] = neighbor_val
                                if not neighbor_cons.pred(temp_assignment):
                                    count += 1
                del self.assignment[var]
                value_counts.append((count, val))
            value_counts.sort() # Sort by the count
            return [val for count, val in value_counts]
        else:
            # Default is the domain's natural order
            return self.domains[var]

    def _backtrack(self):
        if len(self.assignment) == len(self.vars):
            yield dict(self.assignment)
            return

        var = self._select_unassigned_variable()

        for val in self._get_ordered_values(var):
            self.assignment[var] = val
            if self._consistent_with_local(var, self.assignment):
                # Forward check
                pruned = []
                ok = True
                unassigned_neighbors = [
                    v for c in self.cons_by_var[var] for v in c.scope
                    if v != var and v not in self.assignment
                ]
                
                for w in unassigned_neighbors:
                    removed = []
                    for vv in list(self.domains[w]):
                        self.assignment[w] = vv
                        if not self._consistent_with_local(w, self.assignment):
                            self.domains[w].remove(vv)
                            removed.append(vv)
                        del self.assignment[w]
                    if removed:
                        pruned.append((w, removed))
                    if not self.domains[w]:
                        ok = False; break
                
                if ok:
                    yield from self._backtrack()
                else:
                    self.backtracks += 1
                
                # Undo pruning
                for w, removed in pruned:
                    self.domains[w].extend(removed)
            else:
                self.backtracks += 1
            
            del self.assignment[var]