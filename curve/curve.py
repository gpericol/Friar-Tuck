class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class DateError(Error):
    def __init__(self, message):
        self.message = message

class Curve:
    def __init__(self, values):
        self.name = values["name"]
        self.description = values["description"]
        self.points = [(point["hour"]*3600, point["temperature"]) for point in sorted(values["curve"], key = lambda p: p["hour"])]                
            
    def get_name(self):
        return self.name

    def get_description(self):
        return self.description

    def get_start_temperature(self):
        return self.points[0][1]

    def calculate_temperature(self, start_time, current_time):
        delta_time = current_time - start_time

        if delta_time < 0:
            raise DateError("start time is bigger than actual time")

        # find range
        found = False

        for i in range(1, len(self.points)):
            lower_point = self.points[i-1]
            upper_point = self.points[i]

            if delta_time >= lower_point[0] and delta_time < upper_point[0]:
                found = True
                break
        
        # out from limit
        if not found:
            return upper_point[1]

        # calculate y3 given x3 from a line that passes on (x1, y1) and (x2, y2)
        # line formula: y = m*x + q
        # slope: m = (y2 - y1) / (x2 - x1)
        # intercept: q = y1 - (m * x1)
        # y3 = m * x3 + q

        slope = (upper_point[1] - lower_point[1]) / (upper_point[0] - lower_point[0])
        intercept = lower_point[1] - (slope * lower_point[0])

        return round((slope * delta_time) + intercept, 1)