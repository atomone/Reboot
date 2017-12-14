#! /usr/bin/env python

# Pixelman 3 - PyMike's Entry for Ludum Dare 11
# Copyright (C) 2007  PyMike
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

# -------------------------------------
# Controls:
# -------------------------------------
# Move            -  Arrow Keys
# Jump            -  Space, Up, Z
# Back out        -  Escape
# Choose option   -  Enter/Return
# Scroll options  -  Up and Down Arrows
# Warp to level   -  1-5
# -------------------------------------

import pygame, sys, os
from pygame.locals import *

import binascii
from cStringIO import StringIO

level1 = """
++++++++++++++++++++++++++++++++++++++++
++++++++++++++++++++++++++++++++++++++++
++++++++++++++++++++++++++++++++++++++++
+---++++++----+++++++-----++++++++++++++
------------------------------++++++++++
----------------------------------------
----------------------------------------
------oo--------------------------------
------oo-------------------------oo-----
-------------oooo----------------oo-----
------++-----oooo-----------------------
P---++++-------G-----------------++----+
++++++++--++++++++++--+------+--++++-+++
++++++++--++++++++++--+--oo--+++++++-+++
++++++++SS++++++++++SS+SS++SS+++++++S+++
"""

level2 = """
++++++++++++++++++++++++++++++++++++++++++++++++
++++++++++++++++++++++++++++++++++++++++++++++++
++++++++++++++++++++++---+++++++++++++++----++++
+++++++++++++++----------+++++++++++-----------+
-----++++---------------------+++++-------------
--------------------------------++--------------
------------------------------------------------
------------------------------------------------
------------------------------------------------
P-----------------------------------------------
+-------oo------------o-----G-----o--oo---------
+-------oo---------+--+-----------+--oo---------
++++--------++---+++--+o--------oo+--------++---
++++++SS++--++-+++++--++oooo--+++++--++++++++---
++++++++++SS++S+++++SS++++++SS+++++SS+++++++++++
"""

level3 = """
++++++++++++++++++++++++++++++++++++++++++++++++
+++-++++++++++++++++++++++++++++++++++++++++++++
++---++++++++++++++++++++++++++++++----+++++++++
+------++++------+++++++++++++++----------++++++
+-------------------+++++++++------------------+
+-----------------------------------G----------+
+----------------oooo--------------------------+
++P---oooo-------++++-------+++----------------+
++++++++++SSS++++++++++SSS++++++++ooo+SS++-----+
++++++++++++++++++++++++++++++++++++++++++----++
-----------------ooo--------------------------++
-----------------ooo--------------------------++
-----------------+++-----ooo---ooo------------++
-------------++++++++++SS+++SS++++--------ooo+++
-------++++SS++++++++++++++++++++++++SSS++++++++
---+++++++++++++++++++++++++++++++++++++++++++++
+o-++++++---------------------------------------
+o-++++-----------o-----------------------------
+o----------------+o--------G------------------o
+o----------------++o---------------++--------o+
+o-----ooo--oooo+++++o-----o---o----+++oooo--o++
++-----+++SS++++++++++++SSS+SSS+SSS++++++++SS+++
+++SS+++++++++++++++++++++++++++++++++++++++++++
++++++++++++++++++++++++++++++++++++++++++++++++
++++++++++++++++++++++++++++++++++++++++++++++++
"""

level4 = """
----------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------
-P--------------------------------------------------------------------------------------------------
-+--------------------------------------------------------------------------------------------------
-+++----+o--------------------------------------------------oo--------------------------------------
---+++--+o--------------------------------------------------oo--------------------------------------
--------+ooo-----------o+-------------------------ooo-----------------------------------------------
--------++++--+--+--+--o+-------------G-----------ooo-------++-----------------------G--------------
----------------------oo+------------------+--------------+-----------------------------------------
----------------------+++--+------+---------------+++-----+---------------+--ooo--------------------
---------------------------++++---------+----+ooo------++++---------------+--+++--+--+--+--+oooooooo
------------------------------+------+-------++++----------------ooo---++++----------------+++++++++
-----------------------------------------------------------------+++--------------------------------
"""

level5 = """
-----------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------
--------------------------------------------------oooo++---------------------------------------
-----------------------------------------o--------oooo++---------------------------------------
-----------------------------------------o--------oooo++---------------------------------------
---------G----oo-----------------------o-o-o------ooo+++---------------------------------------
P-------------oo---oo-------------------ooo-------oo++++---------------------------------------
++-----------------oo--------------------o-------++++++----------------------------------------
++oooo--------++------------------------------++++++++-----------------------------------------
++++++--+--+--+++--++-------G------ooo++---+++++++++-------------------------------------------
--++++--------++++++++-----------oo++++--------------------------------------------------------
--------------------++-----------o++++---------------------------------------------------------
---------------------++----------++------------------------------------------------------------
----------------------+++--+--+--+--------------------------------------o---------------G------
-----------------------------------------------------------------------o+----------------------
-----------------------------------------------------------o---------oo++--------oo------oooooo
-----------------------------------------o-----o-----o--o--+--o-----o++++SS++----oo--++--++++++
-----------------------------------------+--o--+--o--+--+-----+-----+++++++++++-----+++SS++++++
--------------------------------------------+-----+--------------o--------+++++++SS++++++++++++
-----------------------------------------------------------------+-------------++++++--++++----
"""

player_anim0 = """
------+++++-----
----+++++++++---
---+++++++++++--
--+++++++++++++-
--++++--+++--++-
-+++++--+++--++-
+++++++++++++++-
++++++++++++++++
++++++++++++++++
++++++-+++++-+++
+++++++-----++++
+-++++++++++++++
--++++++++++++-+
---++++++++++---
---++-----++----
--+++++--+++++--
"""
player_anim1 = """
------+++++-----
----+++++++++---
---+++++++++++--
--+++++++++++++-
--++++--+++--++-
-+++++--+++--++-
+++++++++++++++-
++++++++++++++++
++++++++++++++++
++++++-+++++-+++
+++++++-----++++
+-++++++++++++++
--++++++++++++-+
---++++++++++---
--+++++---++----
---------+++++--
"""
player_anim2 = """
------+++++-----
----+++++++++---
---+++++++++++--
--+++++++++++++-
--++++--+++--++-
-+++++--+++--++-
+++++++++++++++-
++++++++++++++++
++++++++++++++++
++++++-+++++-+++
+++++++-----++++
+-++++++++++++++
--++++++++++++-+
---++++++++++---
---++----+++++--
--+++++---------
"""
spikes_img = """
--+---+---+---+-
--+---+---+---+-
--+---+---+---+-
--+---+---+---+-
-+++-+++-+++-+++
-+++-+++-+++-+++
-+++-+++-+++-+++
-+++-+++-+++-+++
-+++-+++-+++-+++
-+++-+++-+++-+++
-+++-+++-+++-+++
-+++-+++-+++-+++
++++++++++++++++
++++++++++++++++
++++++++++++++++
++++++++++++++++
"""

ghostie_img = """
------+++++-----
----+++++++++---
---+++++++++++--
--+++++++++++++-
-+++++--+++--++-
+++++++--+--++++
++++++++-+-+++++
++++++++++++++++
-++++-+++++++-++
--++++--+++--++-
---+++++---++++-
----++++++++++--
-----++++++++---
-------++++-----
"""

jump_sound = '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\n'
coin_sound = 'T2dnUwACAAAAAAAAAACbKgAAAAAAAEgVfO8BHgF2b3JiaXMAAAAAAUSsAAAAAAAAAHcBAAAAAAC4AU9nZ1MAAAAAAAAAAAAAmyoAAAEAAABASoNPEC3//////////////////8kDdm9yYmlzHQAAAFhpcGguT3JnIGxpYlZvcmJpcyBJIDIwMDQwNjI5AAAAAAEFdm9yYmlzKUJDVgEACAAAADFMIMWA0JBVAAAQAABgJCkOk2ZJKaWUoSh5mJRISSmllMUwiZiUicUYY4wxxhhjjDHGGGOMIDRkFQAABACAKAmOo+ZJas45ZxgnjnKgOWlOOKcgB4pR4DkJwvUmY26mtKZrbs4pJQgNWQUAAAIAQEghhRRSSCGFFGKIIYYYYoghhxxyyCGnnHIKKqigggoyyCCDTDLppJNOOumoo4466ii00EILLbTSSkwx1VZjrr0GXXxzzjnnnHPOOeecc84JQkNWAQAgAAAEQgYZZBBCCCGFFFKIKaaYcgoyyIDQkFUAACAAgAAAAABHkRRJsRTLsRzN0SRP8ixREzXRM0VTVE1VVVVVdV1XdmXXdnXXdn1ZmIVbuH1ZuIVb2IVd94VhGIZhGIZhGIZh+H3f933f930gNGQVACABAKAjOZbjKaIiGqLiOaIDhIasAgBkAAAEACAJkiIpkqNJpmZqrmmbtmirtm3LsizLsgyEhqwCAAABAAQAAAAAAKBpmqZpmqZpmqZpmqZpmqZpmqZpmmZZlmVZlmVZlmVZlmVZlmVZlmVZlmVZlmVZlmVZlmVZlmVZlmVZQGjIKgBAAgBAx3Ecx3EkRVIkx3IsBwgNWQUAyAAACABAUizFcjRHczTHczzHczxHdETJlEzN9EwPCA1ZBQAAAgAIAAAAAABAMRzFcRzJ0SRPUi3TcjVXcz3Xc03XdV1XVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVYHQkFUAAAQAACGdZpZqgAgzkGEgNGQVAIAAAAAYoQhDDAgNWQUAAAQAAIih5CCa0JrzzTkOmuWgqRSb08GJVJsnuamYm3POOeecbM4Z45xzzinKmcWgmdCac85JDJqloJnQmnPOeRKbB62p0ppzzhnnnA7GGWGcc85p0poHqdlYm3POWdCa5qi5FJtzzomUmye1uVSbc84555xzzjnnnHPOqV6czsE54Zxzzonam2u5CV2cc875ZJzuzQnhnHPOOeecc84555xzzglCQ1YBAEAAAARh2BjGnYIgfY4GYhQhpiGTHnSPDpOgMcgppB6NjkZKqYNQUhknpXSC0JBVAAAgAACEEFJIIYUUUkghhRRSSCGGGGKIIaeccgoqqKSSiirKKLPMMssss8wyy6zDzjrrsMMQQwwxtNJKLDXVVmONteaec645SGultdZaK6WUUkoppSA0ZBUAAAIAQCBkkEEGGYUUUkghhphyyimnoIIKCA1ZBQAAAgAIAAAA8CTPER3RER3RER3RER3RER3P8RxREiVREiXRMi1TMz1VVFVXdm1Zl3Xbt4Vd2HXf133f141fF4ZlWZZlWZZlWZZlWZZlWZZlCUJDVgEAIAAAAEIIIYQUUkghhZRijDHHnINOQgmB0JBVAAAgAIAAAAAAR3EUx5EcyZEkS7IkTdIszfI0T/M00RNFUTRNUxVd0RV10xZlUzZd0zVl01Vl1XZl2bZlW7d9WbZ93/d93/d93/d93/d939d1IDRkFQAgAQCgIzmSIimSIjmO40iSBISGrAIAZAAABACgKI7iOI4jSZIkWZImeZZniZqpmZ7pqaIKhIasAgAAAQAEAAAAAACgaIqnmIqniIrniI4oiZZpiZqquaJsyq7ruq7ruq7ruq7ruq7ruq7ruq7ruq7ruq7ruq7ruq7ruq7rukBoyCoAQAIAQEdyJEdyJEVSJEVyJAcIDVkFAMgAAAgAwDEcQ1Ikx7IsTfM0T/M00RM90TM9VXRFFwgNWQUAAAIACAAAAAAAwJAMS7EczdEkUVIt1VI11VItVVQ9VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV1TRN0zSB0JCVAAAZAAAjQQYZhBCKcpBCbj1YCDHmJAWhOQahxBiEpxAzDDkNInSQQSc9uJI5wwzz4FIoFURMg40lN44gDcKmXEnlOAhCQ1YEAFEAAIAxyDHEGHLOScmgRM4xCZ2UyDknpZPSSSktlhgzKSWmEmPjnKPSScmklBhLip2kEmOJrQAAgAAHAIAAC6HQkBUBQBQAAGIMUgophZRSzinmkFLKMeUcUko5p5xTzjkIHYTKMQadgxAppRxTzinHHITMQeWcg9BBKAAAIMABACDAQig0ZEUAECcA4HAkz5M0SxQlSxNFzxRl1xNN15U0zTQ1UVRVyxNV1VRV2xZNVbYlTRNNTfRUVRNFVRVV05ZNVbVtzzRl2VRV3RZV1bZl2xZ+V5Z13zNNWRZV1dZNVbV115Z9X9ZtXZg0zTQ1UVRVTRRV1VRV2zZV17Y1UXRVUVVlWVRVWXZlWfdVV9Z9SxRV1VNN2RVVVbZV2fVtVZZ94XRVXVdl2fdVWRZ+W9eF4fZ94RhV1dZN19V1VZZ9YdZlYbd13yhpmmlqoqiqmiiqqqmqtm2qrq1bouiqoqrKsmeqrqzKsq+rrmzrmiiqrqiqsiyqqiyrsqz7qizrtqiquq3KsrCbrqvrtu8LwyzrunCqrq6rsuz7qizruq3rxnHrujB8pinLpqvquqm6um7runHMtm0co6rqvirLwrDKsu/rui+0dSFRVXXdlF3jV2VZ921fd55b94WybTu/rfvKceu60vg5z28cubZtHLNuG7+t+8bzKz9hOI6lZ5q2baqqrZuqq+uybivDrOtCUVV9XZVl3zddWRdu3zeOW9eNoqrquirLvrDKsjHcxm8cuzAcXds2jlvXnbKtC31jyPcJz2vbxnH7OuP2daOvDAnHjwAAgAEHAIAAE8pAoSErAoA4AQAGIecUUxAqxSB0EFLqIKRUMQYhc05KxRyUUEpqIZTUKsYgVI5JyJyTEkpoKZTSUgehpVBKa6GU1lJrsabUYu0gpBZKaS2U0lpqqcbUWowRYxAy56RkzkkJpbQWSmktc05K56CkDkJKpaQUS0otVsxJyaCj0kFIqaQSU0mptVBKa6WkFktKMbYUW24x1hxKaS2kEltJKcYUU20txpojxiBkzknJnJMSSmktlNJa5ZiUDkJKmYOSSkqtlZJSzJyT0kFIqYOOSkkptpJKTKGU1kpKsYVSWmwx1pxSbDWU0lpJKcaSSmwtxlpbTLV1EFoLpbQWSmmttVZraq3GUEprJaUYS0qxtRZrbjHmGkppraQSW0mpxRZbji3GmlNrNabWam4x5hpbbT3WmnNKrdbUUo0txppjbb3VmnvvIKQWSmktlNJiai3G1mKtoZTWSiqxlZJabDHm2lqMOZTSYkmpxZJSjC3GmltsuaaWamwx5ppSi7Xm2nNsNfbUWqwtxppTS7XWWnOPufVWAADAgAMAQIAJZaDQkJUAQBQAAEGIUs5JaRByzDkqCULMOSepckxCKSlVzEEIJbXOOSkpxdY5CCWlFksqLcVWaykptRZrLQAAoMABACDABk2JxQEKDVkJAEQBACDGIMQYhAYZpRiD0BikFGMQIqUYc05KpRRjzknJGHMOQioZY85BKCmEUEoqKYUQSkklpQIAAAocAAACbNCUWByg0JAVAUAUAABgDGIMMYYgdFQyKhGETEonqYEQWgutddZSa6XFzFpqrbTYQAithdYySyXG1FpmrcSYWisAAOzAAQDswEIoNGQlAJAHAEAYoxRjzjlnEGLMOegcNAgx5hyEDirGnIMOQggVY85BCCGEzDkIIYQQQuYchBBCCKGDEEIIpZTSQQghhFJK6SCEEEIppXQQQgihlFIKAAAqcAAACLBRZHOCkaBCQ1YCAHkAAIAxSjkHoZRGKcYglJJSoxRjEEpJqXIMQikpxVY5B6GUlFrsIJTSWmw1dhBKaS3GWkNKrcVYa64hpdZirDXX1FqMteaaa0otxlprzbkAANwFBwCwAxtFNicYCSo0ZCUAkAcAgCCkFGOMMYYUYoox55xDCCnFmHPOKaYYc84555RijDnnnHOMMeecc845xphzzjnnHHPOOeecc44555xzzjnnnHPOOeecc84555xzzgkAACpwAAAIsFFkc4KRoEJDVgIAqQAAABFWYowxxhgbCDHGGGOMMUYSYowxxhhjbDHGGGOMMcaYYowxxhhjjDHGGGOMMcYYY4wxxhhjjDHGGGOMMcYYY4wxxhhjjDHGGGOMMcYYY4wxxhhjjDHGGFtrrbXWWmuttdZaa6211lprrQBAvwoHAP8HG1ZHOCkaCyw0ZCUAEA4AABjDmHOOOQYdhIYp6KSEDkIIoUNKOSglhFBKKSlzTkpKpaSUWkqZc1JSKiWlllLqIKTUWkottdZaByWl1lJqrbXWOgiltNRaa6212EFIKaXWWostxlBKSq212GKMNYZSUmqtxdhirDGk0lJsLcYYY6yhlNZaazHGGGstKbXWYoy1xlprSam11mKLNdZaCwDgbnAAgEiwcYaVpLPC0eBCQ1YCACEBAARCjDnnnHMQQgghUoox56CDEEIIIURKMeYcdBBCCCGEjDHnoIMQQgghhJAx5hx0EEIIIYQQOucchBBCCKGEUkrnHHQQQgghlFBC6SCEEEIIoYRSSikdhBBCKKGEUkopJYQQQgmllFJKKaWEEEIIoYQSSimllBBCCKWUUkoppZQSQgghlFJKKaWUUkIIoZRQSimllFJKCCGEUkoppZRSSgkhhFBKKaWUUkopIYQSSimllFJKKaUAAIADBwCAACPoJKPKImw04cIDUGjISgCADAAAcdhq6ynWyCDFnISWS4SQchBiLhFSijlHsWVIGcUY1ZQxpRRTUmvonGKMUU+dY0oxw6yUVkookYLScqy1dswBAAAgCAAwECEzgUABFBjIAIADhAQpAKCwwNAxXAQE5BIyCgwKx4Rz0mkDABCEyAyRiFgMEhOqgaJiOgBYXGDIB4AMjY20iwvoMsAFXdx1IIQgBCGIxQEUkICDE2544g1PuMEJOkWlDgIAAAAAAAEAHgAAkg0gIiKaOY4Ojw+QEJERkhKTE5QAAAAAAOABgA8AgCQFiIiIZo6jw+MDJERkhKTE5AQlAAAAAAAAAAAACAgIAAAAAAAEAAAACAhPZ2dTAATpGgAAAAAAAJsqAAACAAAAzPigxhBJRP8JOj09PEBC89HOwKqC3IEL0WrXTamu7IMiWtAEJW6eJjWgT8TNYK4OcIoboADENcGV4txpW8cxF/jVLaprQiEsEAFYQrtJTgnAj02NaD2A8QprACxoAdSBS0il6y7b8eyDvlokpRUaVrVAP7BBC1dDXBO/Hpw/evwU+5Jf/dZ9R0u1jG3vLSaqxANUAoQf72XMOcp5GhYBmoYBkviFH4z3cj2VfrhHkWNV9M8J8YGtrAXAQk+w4aB/AH29WRygAxDCAgB4hAYg7g8kNUDg9ccCAEjwQQfgCchsa9kmBCP778epT/nnsc5NOzs5CYbFYjEMwxDJnJ1iVVXVmEwmIyCtXUhzNEYiQERRjHc6K1fl/nVjXFVxaz5DvABANWcIAGOBHhdBPCtNABBCCGEYxoh/M1v31r7PFGgAQBlMhjfHpQUAAAAAAB0MuAIgTVr2lQfmJqMCAAAA1DsF/DwLAfArQgCAdOmlVzABAGZmY4xpuj6YeB9pNTcuTg7blhIA9pdjAPAMBA9dezCBKNUCQAKZmdft/S9OgeJ4fEAAYD99CQAArG13wpJ/ONqM9PFzJ8oE4oYAqGQBJUw1QYnXUwY97BoUxyKyAoggDoaSAgj7L69TCoIHiPcnbcW2BKRtd4Oy1//t7poASxZQLcUNAwBGtPgKliOlRHBhY8zLeK2HHDhAwx/QFnHuFEgBt+0H6wIA9pQCe8nfnROcZXcIlf5wG6+aAHvFnHTbGjYTe3EDVwMUwZRtwsbuWFC6RTm4X74sFD+OAgAEJFYEAN9vjQGw6G0FmgUAnG13gjJXj3RyAixZCyqB1oAeOAsoYTukFAhkZtpau4q5GMKPFIeOqETjNnUAnqZsSAkAXfDhiWMGPhcAtGmvM+2IaUf1wNQNW6ckAQvsCGYLl4ir4+cjYuC46ZCpYdj7U51mMsRe/8Nxqb7+wr1R6M9/WIxCIb+ICXwbA5Rp/8Mxz8Q+RSgjdMh66FpAg5SXAgTX8+Hz8Vptt07fvN7aaj4xiRp9sNUb1YWWigDj5H5NwXIZjvuHIVj+8LGwBDrY3cjvt/D96kb+X2Df+DSSEpoB7AkAPpAE9nT9HgCAJBQIPHi/BABAEsAA+HcDAAB4waCnfgLgY/r0dKxfF15cupS9ojGm2Ww2qyulFJDM6FIBiDFODs++km0CsIYBHGI8P2uAC8BV5qftwaxSSikAAD4ZaAAAaFoDQAFcAQAAqLYKr726UqAAAACI/zYBAAAAAGhtfvbcmRjVAQCI77c04trX64qrqv6NyeaSkpJnL8UEDgKKZwB/NoAvAoAA4IkDAACAcnT0VG2ysx12rbUaIP8dANJhQhM02QA/AAAAnXWWABcAABBBCuDVSoMJqgHwAh6YHfi5C/jX3PH+2bjefmM28kAYJij2AAD3rUBoAChgA9gL8NwPQBIKBB78GwAAggECeycDAHKEBoArMQcU1G0UOLMFOO4AeAAAAKxz+QQAIAGgds0HQBLgRgC+BQAAgG3Z0AIAKMBPeQAlAOCKGQAAAAAAiHYAAMA/CpQDuNINAAAAAAAAAAAAkg9FAQAAgO8GAQAAexsAAKhaEB4MQBQAAAAAfAKAdAINts4G+DAAALChCmTIQoZbAAAAABH8bQYAAAAuAADISAg3jgJjAAIevlcd/H4I+Lc6uH8OvOfTmI38QhiApt8BABAaAEpo9gJcfzQQjDF4GwNBsAIMgHsnAABAkyUALugnUGCZrcDQHuB3FgBgvQYCABIAsgYeAAAAgAbVAgBAAT9lKrAAgH+wCAAA8NsBDABXAAoAAC4bAAAAAACAXxcAAAAAAACARDcGAAAA8N1BAADkLwCwAQDY/9SMAACSgPQrAH8FABEhoOXVEgAAAL8BgAa/AU22AFQLAAAQAQAAUAEG4AFAABkJXQAALB620OAZAAC8AwA+lxz4uQr4Z3Xs3yPXS7XDZPQLensAwH75kiTQafYC9CSBYIzB2wtPACAJIBjwey8AAEsCxxxQEAAEAABA9v0BAoAAq/9yAAAAkC/vxgAABPDvoIAoAChpjQAAAAC+BXAFcAUAAAC4+dQBAAAAAAAAAD9uBwAAAPy0hQaQAPwF8GcBAN8iAPBzJQAAeAGeBnATwCeA41UBAADwZQCgwStgCWyA3wAAABEAAKBQEBQZFu48BgAAQA2+eJ4FGACQoAHeBdzYr6uAX+6ElvBSvUvCzsPZEF+vfwBwK0kCq8PbYHlCKADeA14CAAJJgF/UAFQSEPoJjFGIsBSAhxT7n3bQAJoAP/NSFQAAP6QDAADA7eMKRAUA+7zQAQAAAAAAAOrdpgEAAAAAAICQ9yoAAAD45UNKA4wwfLX1LH/+hyFy1aVGmx+lZEAN8AU4Ay8QFJNFAACAfVUAqoCdALYlABOwQasFAAAP1IAbAN5lBO8/4heW45m4Jwd/O6vRJyGExlJzsAMBpI+AkHIgAAC8svv90P5GZlQAjGXx07vfdk1LrjLHeop8XHyv2TKfle7PLKuLtWbZfmnJsjgFqEx+cLV/5PMWv3vyWEkAeoHR8BUYd/HfXs1YADifDQAAANPtifjyy6ECAABUA4B9zQQ=\n'
blip_sound = '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\n'


def load_sound(string):
    sound_string = binascii.a2b_base64(string)
    f = StringIO(sound_string)
    sound = pygame.mixer.Sound(f)
    sound.set_volume(0.5)
    return sound

LEVELS = [level1, level2, level3, level4, level5]
ONFULLSCREEN = 0

def imagetostring(filename):
    img = pygame.image.load(filename)
    new = ""
    for y in range(img.get_height()):
        for x in range(img.get_width()):
            pixel = img.get_at((x, y))
            if pixel == (0, 0, 0, 255):
                new += "+"
            elif pixel == (255, 255, 0, 255):
                new += "o"
            elif pixel == (255, 0, 0, 255):
                new += "P"
            elif pixel == (0, 0, 255, 255):
                new += "S"
            elif pixel == (0, 255, 0, 255):
                new += "G"
            else:
                new += "-"
        new += "\n"
    return new

def image(color, shape="block", pixelstring=None):
    img = pygame.Surface((16, 16))
    if shape == "block":
        img.fill(Color(color))
    if shape == "circle":
        pygame.draw.ellipse(img, Color(color), (1, 1, 14, 14))
        img.set_colorkey((0, 0, 0), RLEACCEL)
    if pixelstring:
        img.set_colorkey((0, 0, 0), RLEACCEL)
        x=0
        y=-1
        for line in pixelstring.split("\n"):
            for char in line:
                if char == "+":
                    img.fill(Color(color), (x, y, 1, 1))
                x += 1
            y += 1
            x = 0
    return img

def speed_to_side(dx,dy):
    if abs(dx) > abs(dy): dy = 0
    else: dx = 0
    if dy < 0: return 0
    elif dx > 0: return 1
    elif dy > 0: return 2
    elif dx < 0: return 3
    else: return 0, 0

class Sprite(pygame.sprite.Sprite):

    def __init__(self, img, pos):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = img
        self.rect = self.image.get_rect(topleft = pos)
        self.r = Rect(self.rect[0]*100, self.rect[1]*100, self.rect[2]*100, self.rect[3]*100)
        self.collision_groups = []

    def set_pos(self, x, y):
        self.r.left = x*100
        self.r.top = y*100

    def update_rect(self):
        self.rect.top = self.r.top/100
        self.rect.left = self.r.left/100

    def add_collision_group(self, group):
        self.collision_groups.append(group)

    def move(self, dx, dy, collide=True):
        if collide:
            if dx!=0:
                dx, dummy = self.__move(dx*100, 0)
            if dy!=0:
                dummy, dy = self.__move(0, dy*100)
        else:
            self.r.move_ip(dx*100, dy*100)
        return dx, dy

    def __move(self, dx, dy):
        oldr = self.r
        self.r.move_ip(dx, dy)
        side = speed_to_side(dx, dy)

        for group in self.collision_groups:
            for spr in group:
                if spr.r.colliderect(self.r):
                    if side == 0:
                        self.r.top = spr.r.bottom
                    if side == 1:
                        self.r.right = spr.r.left
                    if side == 2:
                        self.jumping = False
                        self.jump_speed = 0
                        self.r.bottom = spr.r.top
                    if side == 3:
                        self.r.left = spr.r.right
        return self.r.left-oldr.left,self.r.top-oldr.top


class Player(Sprite):

    def __init__(self, pos):

        Sprite.__init__(self, image("#010101", pixelstring=player_anim0, shape=None), pos)
        self.images = [image("#010101", pixelstring=player_anim2, shape=None),
                       image("#010101", pixelstring=player_anim1, shape=None),
                       image("#010101", pixelstring=player_anim0, shape=None)]
        self.rightimgs = self.images
        self.leftimgs = []
        for i in self.images:
            self.leftimgs.append(pygame.transform.flip(i, 1, 0))
        self.jump_speed = 0
        self.fall_speed = 0.4
        self.jumping = False

        self.speed = 0
        self.accel_speed = 0.25
        self.max_speed = 3.5
        self.facing = 1
        self.frame = 0
        self.keys = [K_SPACE, K_UP, K_z]
        self.jump_sound = load_sound(jump_sound)

    def jump(self):
        if not self.jumping:
            self.jump_sound.play()
            self.jumping = True
            self.jump_speed = -6

    def update(self):
        if self.jump_speed > 1:
            self.jumping = True
        moving = 0
        key = pygame.key.get_pressed()
        if self.rect.left < 0:
            self.set_pos(0, self.rect.top)
        if key[K_LEFT]:
            self.facing = -1
            moving = -1
            if self.speed > -self.max_speed:
                self.speed -= self.accel_speed
        elif key[K_RIGHT]:
            self.facing = 1
            moving = 1
            if self.speed < self.max_speed:
                self.speed += self.accel_speed
        else:
            if self.speed > 0:
                self.speed -= self.accel_speed
            if self.speed < 0:
                self.speed += self.accel_speed
        if self.jump_speed < 5:
            if key[self.keys[0]] or key[self.keys[1]] or key[self.keys[2]]:
                self.jump_speed += self.fall_speed
            else:
                self.jump_speed += self.fall_speed+0.3
        self.move(self.speed, self.jump_speed)

        self.frame += 1
        if self.facing > 0:
            self.image = self.rightimgs[2]
        if self.facing < 0:
            self.image = self.leftimgs[2]
        if moving > 0:
            self.image = self.rightimgs[self.frame/4%2]
        if moving < 0:
            self.image = self.leftimgs[self.frame/4%2]

class Ghostie(Sprite):

    def __init__(self, pos):

        Sprite.__init__(self, image("#010101", shape=None, pixelstring=ghostie_img), pos)

        self.leftimg = pygame.transform.flip(image("#010101", shape=None, pixelstring=ghostie_img), 1, 0)
        self.rightimg = image("#010101", shape=None, pixelstring=ghostie_img)

        self.frame = 0
        self.speed = 1
        self.orgcenter = self.rect.centerx
        self.y = self.rect.centery

    def update(self):

        if self.speed > 0:
            self.image = self.rightimg
        if self.speed < 0:
            self.image = self.leftimg
            
        self.move(self.speed, 0)
        self.frame += 1

        if self.frame <= 12:
            self.move(0, 0.25)
        else:
            self.move(0, -0.25)
        self.rect.centery = self.y
        if self.frame >= 24:
            self.frame = 0
        if self.rect.right >= self.orgcenter + 50:
            self.speed = -1
        if self.rect.left <= self.orgcenter - 50:
            self.speed = 1

class Block(Sprite):

    def __init__(self, pos):
        Sprite.__init__(self, image("#890000"), pos)

class Spikes(Sprite):

    def __init__(self, pos):
        Sprite.__init__(self, image("#010101", shape=None, pixelstring=spikes_img), pos)

class Coin(Sprite):

    def __init__(self, pos):
        Sprite.__init__(self, image("#ffff00", "circle"), pos)
        self.images = [image("#ffff00", "circle"),
                       image("#f4f400", "circle"),
                       image("#e9e900", "circle"),
                       image("#f4f400", "circle")]
        self.frame = 0
        self.alpha = 255
        self.dead = False
        self.coin_sound = load_sound(coin_sound)
    def kill(self):
        self.dead = True
    def update(self):
        self.frame += 1
        self.image = self.images[self.frame/4%4]
        if self.dead:
            self.alpha -= 75
        if self.alpha <= 0:
            self.coin_sound.play()
            pygame.sprite.Sprite.kill(self)
        self.image.set_alpha(self.alpha)

class Camera(object):

    def __init__(self, screen, sprite_to_center_on, world_size):
        self.sprite = sprite_to_center_on
        self.rect = screen.get_rect()
        self.world_rect = Rect(0, 0, world_size[0], world_size[1])

    def update(self):
        if self.sprite.rect.centerx > self.rect.centerx + 25:
            self.rect.centerx = self.sprite.rect.centerx - 25
        if self.sprite.rect.centerx < self.rect.centerx - 25:
            self.rect.centerx = self.sprite.rect.centerx + 25
        if self.sprite.rect.centery > self.rect.centery + 25:
            self.rect.centery = self.sprite.rect.centery - 25
        if self.sprite.rect.centery < self.rect.centery - 25:
            self.rect.centery = self.sprite.rect.centery + 25
        self.rect.clamp_ip(self.world_rect)
        
    def draw_group(self, surface, group):
        for sprite in group.sprites():
            if sprite.rect.left <= self.rect.right and sprite.rect.right >= self.rect.left:
                if sprite.rect.top <= self.rect.bottom and sprite.rect.bottom >= self.rect.top:
                    surface.blit(sprite.image, self.sprite_rect(sprite))
            
    def update_group(self, group):
        for sprite in group.sprites():
            if sprite.rect.left <= self.rect.right and sprite.rect.right >= self.rect.left:
                if sprite.rect.top <= self.rect.bottom and sprite.rect.bottom >= self.rect.top:
                    sprite.update()
                    sprite.update_rect()

    def sprite_rect(self, actor):
        return pygame.Rect(actor.rect.x - self.rect.x, actor.rect.y - self.rect.y, actor.rect.w, actor.rect.h)

class Level:

    def __init__(self, level=level1):
        self.level = level
        self.x = 0
        self.y = -16
        for line in self.level.split("\n"):
            for char in line:
                if char == "+":
                    Block((self.x, self.y))
                if char == "P":
                    self.player = Player((self.x, self.y))
                if char == "o":
                    Coin((self.x, self.y))
                if char == "S":
                    Spikes((self.x, self.y))
                if char == "G":
                    Ghostie((self.x, self.y))
                self.x += 16
            self.y += 16
            self.x = 0

    def get_size(self):
        lines = self.level.split("\n")
        line = lines[1]
        width = (len(line))*16
        height = (len(lines)-2)*16
        return [width, height]

def next_level(levelnum):
    try:
        levelnum += 1
        lvl = LEVELS[levelnum-1]
    except:
        return None
    level = Level(lvl)
    return level, levelnum


def Menu(screen):

    screen = screen
    font = pygame.font.SysFont("courier", 32, bold=True)
    font2 = pygame.font.SysFont("courier", 20, bold=True)
    font3 = pygame.font.SysFont("courier", 12, bold=True)

    player = image("#010101", shape=None, pixelstring=player_anim0)
    player = pygame.transform.scale(player, [player.get_width()*6, player.get_height()*6])
    cursor = image("#010101", shape="circle")
    cursorpos = 150
    option = 1
    sound = load_sound(blip_sound)
    clock = pygame.time.Clock()
    global ONFULLSCREEN

    while 1:

        clock.tick(30)
        for e in pygame.event.get():
            if e.type == QUIT:
                pygame.quit()
                sys.exit()
            if e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if e.key == K_DOWN:
                    sound.play()
                    option = 2
                if e.key == K_UP:
                    sound.play()
                    option = 1
                if e.key == K_RETURN:
                    sound.play()
                    if option == 1:
                        Intro(screen)
                        game = Game(screen)
                        game.main_loop()
                    if option == 2:
                        pygame.quit()
                        return
                if e.key == K_f:
                    ONFULLSCREEN ^= 1
                    if ONFULLSCREEN:
                        pygame.display.set_mode((320, 240), FULLSCREEN)
                    else:
                        pygame.display.set_mode((320, 240))

        if option == 1:
            cursorpos = 150
        else:
            cursorpos = 170

        screen.fill(Color("#c1c1c1"))
        pygame.draw.rect(screen, Color("#890000"), (55, 25, 210, 45), 5)
        pygame.draw.rect(screen, Color("#890000"), (0, 227, 320, 32))
        ren = font.render("Pixelman 3", 1, Color("#000000"))
        screen.blit(ren, (161-ren.get_width()/2, 31))
        ren = font.render("Pixelman 3", 1, Color("#ffffff"))
        screen.blit(ren, (160-ren.get_width()/2, 30))

        ren = font3.render("Copyright (C) 2008", 1, Color("#000000"))
        screen.blit(ren, (160-ren.get_width()/2, 85))
        ren = font3.render("Created by PyMike for LD XI", 1, Color("#000000"))
        screen.blit(ren, (160-ren.get_width()/2, 100))

        ren = font2.render("New Game", 1, Color("#000000"))
        screen.blit(ren, (140, 145))
        ren = font2.render("Quit Game", 1, Color("#000000"))
        screen.blit(ren, (140, 165))
        screen.blit(player, (10, 132))
        screen.blit(cursor, (120, cursorpos))
        pygame.display.flip()


def Intro(screen):

    screen = screen
    font = pygame.font.SysFont("courier", 32, bold=True)
    font2 = pygame.font.SysFont("courier", 16, bold=True)
    font3 = pygame.font.SysFont("courier", 12, bold=True)

    player = image("#010101", shape=None, pixelstring=player_anim0)
    player = pygame.transform.scale(player, [player.get_width()*6, player.get_height()*6])
    cursor = image("#010101", shape="circle")
    option = 1
    sound = load_sound(blip_sound)
    clock = pygame.time.Clock()
    ypos = 240
    global ONFULLSCREEN
    text = ["Oh noes! Pixelman is not",
            "drawing pixels fast enough!",
            "Help Pixelman speed through",
            "the levels before his owner",
            "discards the computer monitor",
            "for being a minimalist!"]

    while 1:

        clock.tick(60)
        for e in pygame.event.get():
            if e.type == QUIT:
                pygame.quit()
                sys.exit()
            if e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    return
                if e.key == K_RETURN:
                    sound.play()
                    return
                if e.key == K_f:
                    ONFULLSCREEN ^= 1
                    if ONFULLSCREEN:
                        pygame.display.set_mode((320, 240), FULLSCREEN)
                    else:
                        pygame.display.set_mode((320, 240))

        screen.fill(Color("#c1c1c1"))
        ren = font.render("Prologue", 1, Color("#000000"))
        screen.blit(ren, (160-ren.get_width()/2, 20))
        ypos = 75
        for line in text:
            ren = font2.render(line, 1, (0, 0, 0))
            screen.blit(ren, (160-ren.get_width()/2, ypos))
            ypos += font2.get_height()
        ren = font3.render("Press Enter To Start", 1, Color("#000000"))
        screen.blit(ren, (160-ren.get_width()/2, 210))
        pygame.display.flip()

def Outro(screen, final_score=0):

    screen = screen
    font = pygame.font.SysFont("courier", 32, bold=True)
    font2 = pygame.font.SysFont("courier", 16, bold=True)
    font3 = pygame.font.SysFont("courier", 12, bold=True)

    player = image("#010101", shape=None, pixelstring=player_anim0)
    player = pygame.transform.scale(player, [player.get_width()*6, player.get_height()*6])
    cursor = image("#010101", shape="circle")
    option = 1
    sound = load_sound(blip_sound)
    clock = pygame.time.Clock()
    ypos = 240
    global ONFULLSCREEN
    text = ["Hurray! You saved Pixelman",
            "from being scrapped!",
            "Nice work!",
            "",
            "Final Score:",
            "%09d" % final_score]

    while 1:

        clock.tick(60)
        for e in pygame.event.get():
            if e.type == QUIT:
                pygame.quit()
                sys.exit()
            if e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    return
                if e.key == K_RETURN:
                    sound.play()
                    return
                if e.key == K_f:
                    ONFULLSCREEN ^= 1
                    if ONFULLSCREEN:
                        pygame.display.set_mode((320, 240), FULLSCREEN)
                    else:
                        pygame.display.set_mode((320, 240))

        screen.fill(Color("#c1c1c1"))
        ren = font.render("You won!", 1, Color("#000000"))
        screen.blit(ren, (160-ren.get_width()/2, 20))
        ypos = 75
        for line in text:
            ren = font2.render(line, 1, (0, 0, 0))
            screen.blit(ren, (160-ren.get_width()/2, ypos))
            ypos += font2.get_height()
        ren = font3.render("Press Enter to Exit to Title Screen", 1, Color("#000000"))
        screen.blit(ren, (160-ren.get_width()/2, 210))
        pygame.display.flip()


class Game:

    def __init__(self, screen):

        self.screen = screen
        self.all = pygame.sprite.RenderUpdates()
        self.blocks = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.spikes = pygame.sprite.Group()
        self.ghosties = pygame.sprite.Group()

        Player.containers = self.all
        Block.containers = self.all, self.blocks
        Coin.containers = self.all, self.coins
        Spikes.containers = self.all, self.spikes
        Ghostie.containers = self.all, self.ghosties

        self.clock = pygame.time.Clock()
        self.level = Level()
        self.player = self.level.player
        self.player.add_collision_group(self.blocks)
        self.camera = Camera(self.screen, self.player, self.level.get_size())
        self.lvl = 1
        self.font = pygame.font.SysFont("courier", 12, bold=True)
        self.font2 = pygame.font.SysFont("courier", 32, bold=True)
        self.score = 0
        self.lives = 5
        self.done = False
        self.coin_sound = load_sound(coin_sound)
        self.highscore = 0
        self.paused = False
        self.time = 0
        self.final_score = 0

    def draw(self):
        self.screen.fill(Color("#c1c1c1"))
        self.camera.draw_group(self.screen, self.all)
        ren1 = self.font.render("FPS: %d/60" % self.clock.get_fps(), 1, Color("#000000"))
        ren2 = self.font.render("FPS: %d/60" % self.clock.get_fps(), 1, Color("#ffffff"))
        self.screen.blit(ren1, (6, 221))
        self.screen.blit(ren2, (5, 220))
        ren1 = self.font.render("Score: %d" % self.score, 1, Color("#000000"))
        ren2 = self.font.render("Score: %d" % self.score, 1, Color("#ffffff"))
        self.screen.blit(ren1, (11, 6))
        self.screen.blit(ren2, (10, 5))
        ren1 = self.font.render("Level: %d" % self.lvl, 1, Color("#000000"))
        ren2 = self.font.render("Level: %d" % self.lvl, 1, Color("#ffffff"))
        self.screen.blit(ren1, (246, 6))
        self.screen.blit(ren2, (245, 5))
        ren1 = self.font.render("Lives x%d" % self.lives, 1, Color("#000000"))
        ren2 = self.font.render("Lives x%d" % self.lives, 1, Color("#ffffff"))
        self.screen.blit(ren1, (131, 6))
        self.screen.blit(ren2, (130, 5))
        ren1 = self.font.render("Time: %d" % self.time, 1, Color("#000000"))
        ren2 = self.font.render("Time: %d" % self.time, 1, Color("#ffffff"))
        self.screen.blit(ren1, (11, 21))
        self.screen.blit(ren2, (10, 20))
        self.final_score = (self.score - int(self.time))*self.lives
        if self.lives <= 0 and not self.player.alive() and not self.done:
            ren1 = self.font2.render("Game Over!", 1, Color("#000000"))
            ren2 = self.font2.render("Game Over!", 1, Color("#ffffff"))
            self.screen.blit(ren1, (160-ren1.get_width()/2 + 2, 120-ren1.get_height()/2 + 2))
            self.screen.blit(ren2, (160-ren2.get_width()/2, 120-ren2.get_height()/2))                

    def hit_screen(self):
        self.draw()
        ren1 = self.font2.render("You Crashed!", 1, Color("#000000"))
        ren2 = self.font2.render("You Crashed!", 1, Color("#ffffff"))
        self.screen.blit(ren1, (160-ren1.get_width()/2 + 2, 120-ren1.get_height()/2 + 2))
        self.screen.blit(ren2, (160-ren2.get_width()/2, 120-ren2.get_height()/2))                
        pygame.display.flip()
        pygame.time.wait(1000)

    def main_loop(self):

        global ONFULLSCREEN
        while 1:

            self.clock.tick(60)
            if self.player.alive():
                self.time += 0.015
            for e in pygame.event.get():
                if e.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if e.type == KEYDOWN:
                    if e.key == K_ESCAPE:
                        return
                    if e.key in self.player.keys:
                        self.player.jump()
                    if e.key == K_1:
                        self.lvl = 0
                        self.next_level()
                    if e.key == K_2:
                        self.lvl = 1
                        self.next_level()
                    if e.key == K_3:
                        self.lvl = 2
                        self.next_level()
                    if e.key == K_4:
                        self.lvl = 3
                        self.next_level()
                    if e.key == K_5:
                        self.lvl = 4
                        self.next_level()
                    if e.key == K_p:
                        self.paused ^= 1
                    if e.key == K_f:
                        ONFULLSCREEN ^= 1
                        if ONFULLSCREEN:
                            pygame.display.set_mode((320, 240), FULLSCREEN)
                        else:
                            pygame.display.set_mode((320, 240))
                        pygame.time.wait(1500)
            while self.paused:
                self.clock.tick(20)
                for e in pygame.event.get():
                    if e.type == QUIT:
                        pygame.quit()
                        return
                    if e.type == KEYDOWN:
                        if e.key == K_ESCAPE:
                            return
                        if e.key == K_p:
                            self.paused ^= 1

            for sprite in self.all.sprites():
                if isinstance(sprite, Coin):
                    sprite.update()
                if sprite.rect.left <= self.camera.rect.right and sprite.rect.right >= self.camera.rect.left:
                    if sprite.rect.top <= self.camera.rect.bottom and sprite.rect.bottom >= self.camera.rect.top:
                        if not isinstance(sprite, Coin):
                            sprite.update()
                        sprite.update_rect()
                        if isinstance(sprite, Coin):
                            if self.player.rect.colliderect(sprite.rect) and not sprite.dead:
                                sprite.kill()
                                self.score += 25
                        if isinstance(sprite, Spikes):
                            if self.player.rect.colliderect(sprite.rect):
                                self.player.kill()
                        if isinstance(sprite, Ghostie):
                            if self.player.rect.colliderect(sprite.rect):
                                self.player.kill()

            if self.score > self.highscore:
                self.highscore = self.score
            if not self.player.alive() and self.lives > 0 and not self.done:
                self.hit_screen()
                self.score = 0
                self.lvl -= 1
                self.lives -= 1
                self.next_level()
            if self.player.rect.right >= self.level.get_size()[0] and not self.done:
                self.player.kill()
                self.next_level()
            if self.player.rect.top >= self.level.get_size()[1]:
                self.player.kill()
            if self.done:
                Outro(self.screen, self.final_score)
                return
            self.camera.update()
            self.draw()
            pygame.display.flip()

    def next_level(self):
        lvl = next_level(self.lvl)
        if lvl == None:
            self.done = True
        else:
            self.clear_sprites()
            self.level, self.lvl = next_level(self.lvl)
            self.player = self.level.player
            self.player.add_collision_group(self.blocks)
            self.camera = Camera(self.screen, self.player, self.level.get_size())            

    def clear_sprites(self):
        for sprite in self.all.sprites():
            pygame.sprite.Sprite.kill(sprite)

def main():
    if sys.platform in ("win32", "win64"):
        os.environ["SDL_VIDEO_CENTERED"] = "1"
    pygame.init()
    pygame.display.set_caption("Pixelman 3 - PyMike LD48")
    pygame.mouse.set_visible(0)
    screen = pygame.display.set_mode((320, 240))
    Menu(screen)

if __name__ == "__main__":
    main()
