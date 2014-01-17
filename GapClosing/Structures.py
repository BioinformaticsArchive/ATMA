class Token:
    ID          = None
    SIZE        = None
    SHAPE       = None
    EP1         = None
    EP2         = None


class EndPoint:
    Token       = None
    Position    = None
    Thickness   = None
    Orientation = None

class Gap:
    EP1         = None
    EP2         = None
    Prob_Conn   = None
    Prob_Node   = None
    RNode       = None
