# NetworkX Exception Hierarchy — 1:1 compatible


class NetworkXException(Exception):
    """Base class for exceptions in NetworkX."""


class NetworkXError(NetworkXException):
    """Exception for a serious error in NetworkX."""


class NetworkXPointlessConcept(NetworkXException):
    """Raised when a null graph is drawn w/o a layout algorithm."""


class NetworkXAlgorithmError(NetworkXException):
    """Exception for unexpected termination of algorithms."""


class NetworkXUnfeasible(NetworkXAlgorithmError):
    """Exception raised by algorithms trying to solve a problem
    instance that has no feasible solution."""


class NetworkXNoPath(NetworkXUnfeasible):
    """Exception for algorithms that should return a path when running
    on graphs where such a path does not exist."""


class NetworkXNoCycle(NetworkXUnfeasible):
    """Exception for algorithms that should return a cycle when running
    on graphs where such a cycle does not exist."""


class NetworkXUnbounded(NetworkXAlgorithmError):
    """Exception raised by algorithms trying to solve a maximization
    or minimization problem instance that is unbounded."""


class NodeNotFound(NetworkXException):
    """Exception raised if requested node is not present in the graph."""


class HasACycle(NetworkXException):
    """Raised if a graph has a cycle when an algorithm expects it not to."""


class PowerIterationFailedConvergence(NetworkXAlgorithmError):
    """Raised when power iteration fails to converge within max iterations."""

    def __init__(self, num_iterations: int, *args: object) -> None:
        msg = f"power iteration failed to converge within {num_iterations} iterations"
        super().__init__(msg, *args)
        self.num_iterations = num_iterations


class ExceededMaxIterations(NetworkXAlgorithmError):
    """Raised if a loop exceeds the maximum number of iterations."""


class AmbiguousSolution(NetworkXException):
    """Raised if more than one valid solution exists for an intermediary step
    of an algorithm."""
