�
���^c           @   s   d  d d �  �  YZ  d S(   t   my_w2nc           B   s#  e  Z i d  d 6d d 6d d 6d d 6d d	 6d
 d 6d d 6d d 6d d 6d d 6d d 6d d 6d d 6d d 6d d 6d d 6d  d! 6d" d# 6d$ d% 6d& d' 6Z i	 d( d) 6d* d+ 6d( d, 6d- d. 6d/ d0 6d1 d2 6d3 d4 6d5 d6 6d7 d8 6Z i d9 d: 6d; d< 6d= d> 6d? d@ 6dA dB 6Z dC �  Z dD �  Z dE �  Z RS(F   i   t   onei   t   eleveni   t   twoi   t   twelvei   t   threei   t   thirteeni   t   fouri   t   fourteeni   t   fivei   t   fifteeni   t   sixi   t   sixteeni   t   seveni   t	   seventeeni   t   eighti   t   eighteeni	   t   ninei
   t   teni   t   nineteeng      �?t   halfi   t   nhalfi   t   twentyt   thirtyi(   t   fortyi2   t   fiftyi<   t   sixtyiF   t   seventyiP   t   eightyiZ   t   ninetyid   t   hundredi�  t   thousandi@B t   millioni ʚ;t   billionI ���   t   trillionc         C   s   d |  _  d  S(   Ns"   This will convert words to numbers(   t   info(   t   self(    (    s]   /home/mady/MEGA/mady/courses/learn_ros_python/ros_ws/src/jarvis/event_finder/w2n_full_text.pyt   __init__)   s    c         C   s�  t  | � t k r! | j �  } n t  | � t k r< | } n  | j d � d } d } d } d  } t } y7x�| t | � k  r`t } t }	 t }
 | | |  j	 j
 �  k r{| d  k r� | } n  t } |  j	 j | | � } | d 7} | t | � k r| | k r| | } qn  | | |  j j
 �  k r�| d  k rA| } n  t }
 | |  j j | | � 9} | d 7} | | } q�ng | | |  j j
 �  k r�| d  k r�| } n  t }
 | } |  j j | | � } | d 7} | | } n  | | |  j j
 �  k r�| d  k r| } n  t }	 | d k rI| |  j j | | � } | d 7} q�t } t | � d t |  j j | | � � d } | d 7} n  |
 r�|	 r�| r�| r�| | } t } q�| } t } n  |
 rm |	 rm | rm | d  k	 r-| | d k r-| } | |  t | � g | | } d } d  } d } q]| | d k rPt } | d 7} q]| d 7} qm qm W| d  k	 r�| } | |  t | � g | | } n  | d  SWn; t k
 r�| } | |  t | � g | | } | d  SXd  S(	   Nt   di    i   ic   s    h s    m t   andi����(   t   typet   strt   splitt   listt   appendt   Nonet   Falset   lent   Truet   __ones__t   keyst   gett
   __groups__t   __tens__t
   IndexError(   R$   t   st   wordst	   new_valuet   countt	   old_valuet   startt   got_andt   not_onet   not_tent	   not_grandt   non_currencyt   end(    (    s]   /home/mady/MEGA/mady/courses/learn_ros_python/ros_ws/src/jarvis/event_finder/w2n_full_text.pyt   find_grands-   s�    	 	
 	
 	
 	.
			"c         C   s�   t  } t | � t k r0 d } | j | � } n  d | k rW | j d d � } t } n  d | k r~ | j d d � } t } n  d | k r� | j d d � } t } n  d	 | k s� d
 | k r� t } n  |  j | � } t } | d  k r� t  } n  | | | f S(   Nt    s   half an hours   0 h 30 ms
   in an hours   an hours   1 hs   and halfR   s    hourst   minutes(   R.   R(   R+   t   joint   replaceR0   RC   R-   (   R$   R7   t   shortt   nR9   t   found(    (    s]   /home/mady/MEGA/mady/courses/learn_ros_python/ros_ws/src/jarvis/event_finder/w2n_full_text.pyt	   find_time�   s(    				 	(   t   __name__t
   __module__R1   R5   R4   R%   RC   RK   (    (    (    s]   /home/mady/MEGA/mady/courses/learn_ros_python/ros_ws/src/jarvis/event_finder/w2n_full_text.pyR       s8   




		ZN(    (   R    (    (    (    s]   /home/mady/MEGA/mady/courses/learn_ros_python/ros_ws/src/jarvis/event_finder/w2n_full_text.pyt   <module>   s    