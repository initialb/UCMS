import random
from retrying import retry


@retry(stop_max_attempt_number=3, wait_fixed=2000)
def do_something_unreliable():
    if random.randint(0, 10) > 1:
        print "Error"
        raise IOError("Broken sauce, everything is hosed!!!111one")
    else:
        return "Awesome sauce!"

print do_something_unreliable()