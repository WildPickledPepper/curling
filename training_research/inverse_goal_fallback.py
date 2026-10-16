"""Action coverage for terminal tasks without a placement or contact anchor."""
from training_research.inverse_goal_search import clip


def unanchored_proposals(scene):
    # An actual OUT_OF_PLAY goal may leave every prior stone stationary. It
    # needs no contact/landing anchor. These are proposals, not claimed exits.
    return [(abs(h)*-.01+.001*abs(w)+.01*(6.-v),clip((v,h,w)),("unanchored",v,h,w))
            for v in (6.,4.2,3.) for h in (-2.23,2.23,0.) for w in (0.,-15.,15.)]
