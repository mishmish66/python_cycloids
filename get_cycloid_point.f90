REAL*8 function get_cycloid_point(pin_count, tooth_dif, pinwheel_r, pin_r, &
      eccentricity, offset_angle, inverted, draw_wobbles, &
      input_wobbles, twist)
implicit none
REAL*8, intent(in) :: pin_count
REAL*8, intent(in) :: tooth_dif
REAL*8, intent(in) :: pinwheel_r
REAL*8, intent(in) :: pin_r
REAL*8, intent(in) :: eccentricity
REAL*8, intent(in) :: offset_angle
REAL*8, intent(in) :: inverted
REAL*8, intent(in) :: draw_wobbles
REAL*8, intent(in) :: input_wobbles
REAL*8, intent(in) :: twist
get_cycloid_point(1, 1) = eccentricity*cos(6.2831853071795865d0* &
      input_wobbles)
get_cycloid_point(2, 1) = eccentricity*sin(6.2831853071795865d0* &
      input_wobbles)
end function
