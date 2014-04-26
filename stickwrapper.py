class StickWrapper(object):
    def __init__(self,realStick):
        self.realStick = realStick
        self.realStick.init()
        if realStick.get_name() == 'Twin USB Joystick':
            self.conversion = [2,1,3,0,6,7,8,9]
        if "XBOX 360" in realStick.get_name():
            self.conversion = [0,1,2,3,4,5,6,7]

    def getAllButtons(self):
        return [self.realStick.get_button(b) for b in self.conversion]

    def getHat(self):
        hat = self.realStick.get_hat(0)
        if hat == (0,0):
            return (int(round(self.realStick.get_axis(0),0)),-int(round(self.realStick.get_axis(1),0)))
        else:
            return hat
