import re
import sys

def advance_time(time_string, minutes_to_adv_str):
    """
    Function to advance the time forwards or backwards depending on input.
    :param time_string: string containing the time to start at
    :param minutes_to_adv: integer to advance the time by
    """
    def decrease_hour(orig_hr, hr_to_change, ampm):
        """Function to decrease hours, and apply math if below 1AM/PM"""
        if ((orig_hr - hr_to_change) < 1):
            new_hr = (12 - (hr_to_change - orig_hr))
            ampm = flip_ampm(ampm)
        else:
            new_hr = (orig_hr - hr_to_change)
        return new_hr,ampm

    def decrease_min(orig_min, min_to_change, hr_to_change):
        """Function to decrease minutes, and apply math if below X:00"""
        if ((orig_min - min_to_change) < 0):
            new_min = (60 - (min_to_change - orig_min))
            hr_to_change += 1
        else:
            new_min = (orig_min - min_to_change)
        return new_min,hr_to_change

    def increase_hour(orig_hr, hr_to_change, ampm):
        """Function to increase hours, and apply math if above 12AM/PM"""
        if ((orig_hr + hr_to_change) > 12):
            new_hr = (hr_to_change - (12 - orig_hr))
            ampm = flip_ampm(ampm)
        else:
            new_hr = (orig_hr + hr_to_change)
        if (new_hr == 12):
            ampm = flip_ampm(ampm)
        return new_hr,ampm

    def increase_min(orig_min, min_to_change, hr_to_change):
        """Function to increase minutes, and apply math if above X:59"""
        if ((orig_min + min_to_change) > 59):
            new_min = (min_to_change - (60 - orig_min))
            hr_to_change += 1
        else:
            new_min = (orig_min + min_to_change)
        return new_min,hr_to_change

    def flip_ampm(ampm):
        if (ampm == "PM"):
            return "AM"
        elif (ampm == "AM"):
            return "PM"
        else:
            return "You seem to have created a new time of day"
    
    # Split the time into hour, minutes, and AM/PM, splitting at : and " "
    orig_hr_str,orig_min_str,ampm = re.split("[: ]", time_string)

    # Verify values are convertable to integerss
    for val in [orig_hr_str, orig_min_str, minutes_to_adv_str]:
        try:
            int_test = int(val)
        except ValueError:
            print "Value " + val + " must be an integer."
            sys.exit(1)
            
    # Actually convert them
    orig_hr = int(orig_hr_str)
    orig_min = int(orig_min_str)
    minutes_to_adv = int(minutes_to_adv_str)

    # Verify hours are not in military/24hr format, and is greater than 01
    if (orig_hr > 12) or (orig_hr <= 0):
        print "Time format is not correct. Please use 12-hour (1 - 12) format, not military time."
        sys.exit(1)
    elif (orig_min < 0) or (orig_min >= 60):
        print "Minute value must be between 0 and 59."
        sys.exit(1)

    # Convert minutes into hour and minutes
    hr_to_change,min_to_change = divmod(abs(minutes_to_adv), 60)

    # Change the time: decrease if provided int was neg, increase if pos.
    # If hour and minute value goes below 1AM/PM or X:00 threshold, apply the formulas 
    #     (12 - (b - a)) and/or (60 - (b -a)) respectively 
    #     (and subtract one extra hour depending on if minutes hits floor).
    if (minutes_to_adv < 0):
        new_min,hr_to_change = decrease_min(orig_min, min_to_change, hr_to_change)
        new_hr,ampm = decrease_hour(orig_hr, hr_to_change, ampm)
    # If hour and minute value goes above 12AM/PM or X:59 threshold, apply the formulas
    #    (b - (12 - a) and/or (b - (60 - a)) respectively
    #    (and add one extra hour depending on if minutes hits ceiling).
    else:
        new_min,hr_to_change = increase_min(orig_min, min_to_change, hr_to_change)
        new_hr,ampm = increase_hour(orig_hr, hr_to_change, ampm)

    new_time = str(new_hr).zfill(2) + ":" + str(new_min).zfill(2) + " " + ampm
    print new_time

def main(time, minutes):
    advance_time(time, minutes)

if __name__ == '__main__':
    if len(sys.argv) == 3:
        main(sys.argv[1], sys.argv[2])
    elif len(sys.argv) == 4:
        # Workaround for if time is not quoted.
        time_str = sys.argv[1] + " " + sys.argv[2]
        main(time_str, sys.argv[3])
    else:
        print "Incorrect arguments. Usage: datetime.py \"<time_string>\" minute_int"
        sys.exit(1)
