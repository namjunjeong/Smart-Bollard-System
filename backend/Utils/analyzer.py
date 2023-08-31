class analyzer:
    def __init__(self, occupy_ratio=30, maintain_frame = 10, target_object = 3):
        self.occupy_ratio = (int(occupy_ratio) if occupy_ratio!= '' else 30)
        self.target_object = (int(target_object) if target_object!='' else 3)
        self.maintain_frame = (int(maintain_frame) if maintain_frame!='' else 10)
        self.counter = 0

    def analyze(self, result):
        maxval = 0
        img_area = result.orig_shape[0] * result.orig_shape[1]
        motordata = result.boxes.data[(result.boxes.data[:,5]==self.target_object).nonzero().squeeze(1)]
        for motor in motordata:
            cur_ratio = (float(motor[2])-float(motor[0]))*(float(motor[3])-float(motor[1]))/img_area * 100
            if cur_ratio > maxval : maxval = cur_ratio
        if maxval > self.occupy_ratio:
            self.counter=self.maintain_frame
        else:
            self.counter -= 1
        return True if self.counter>0 else False