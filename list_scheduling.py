from Queue import PriorityQueue


class Ops(object):

    def __init__(self, ops_type, oid):
        self.id = oid
        self.dep_nodes = []
        self.next_nodes = []
        self.priority = 0
        self.type = ops_type
        self.step = 0

    def get_delay(self):
        if self.type == "mul":
            return 2
        else:
            return 1

    def set_step(self, step):
        self.step = step
        return self.step

    def get_status(self, current_step):
        """
        0 waiting to be executed
        1 executing 
        2 finished
        """
        if self.step == 0:
            return 0
        elif self.step + self.get_delay() > current_step:
            return 1
        else:
            return 2

    def head_node(self):
        if len(self.dep_nodes) == 0:
            return True
        else:
            return False

    def ready(self, current_step):
        i = len(self.dep_nodes)
        for node in self.dep_nodes:
            if node.get_status(current_step) != 2:
                return False
            else:
                i = i - 1
        if i == 0:
            return True

    def get_priority(self):
        if self.priority > 0:
            return self.priority
        else:
            priority = 1
            for op in self.next_nodes:
                if op.get_priority() + op.get_delay() > priority:
                    priority = op.get_priority() + op.get_delay()
            self.priority = priority
            return self.priority


def main():
    ops1 = Ops("mul", 1)
    ops2 = Ops("mul", 2)
    ops3 = Ops("mul", 3)
    ops4 = Ops("sub", 4)
    ops5 = Ops("sub", 5)
    ops6 = Ops("mul", 6)
    ops7 = Ops("mul", 7)
    ops8 = Ops("mul", 8)
    ops9 = Ops("add", 9)
    ops10 = Ops("sub", 10)
    ops11 = Ops("cmp", 11)
    ops3.dep_nodes = [ops1, ops2]
    ops4.dep_nodes = [ops3]
    ops5.dep_nodes = [ops4, ops7]
    ops7.dep_nodes = [ops6]
    ops9.dep_nodes = [ops8]
    ops11.dep_nodes = [ops10]
    ops1.next_nodes = [ops3]
    ops2.next_nodes = [ops3]
    ops3.next_nodes = [ops4]
    ops4.next_nodes = [ops5]
    ops6.next_nodes = [ops7]
    ops7.next_nodes = [ops5]
    ops8.next_nodes = [ops9]
    ops10.next_nodes = [ops11]

    capacity = {"alu": 2, "mul": 2}
    ops_all = set([ops1, ops2, ops3, ops4, ops5, ops6, ops7, ops8, ops9, ops10, ops11])
    step = 1
    ops_waiting = ops_all
    mul_unfinished = set()
    alu_unfinished = set()
    mul_ready = set()
    alu_ready = set()
    mul_schedule = set()
    alu_schedule = set()
    for op in ops_all:
        if op.head_node():
            if op.type == "mul":
                mul_ready.add(op)
            else:
                alu_ready.add(op)
#    for op in ops_all:
#        op.get_priority()
#        print("id: " + str(op.id) + " priority: " + str(op.priority)) 

    print "Start scheduling"
    while len(ops_waiting) > 0:
        """
        update mul_unfinished and alu_unfinished
        """
        mul_finished = set()
        for op in mul_unfinished:
            if op.get_status(step) == 2:
                mul_finished.add(op)

        alu_finished = set()
        for op in alu_unfinished:
            if op.get_status(step) == 2:
                alu_finished.add(op)
                
        mul_unfinished.difference_update(mul_finished)
        alu_unfinished.difference_update(alu_finished)

        """
        update mul_ready and alu_ready
        """
        mul_ready.difference_update(mul_schedule)
        alu_ready.difference_update(alu_schedule)
        finished = mul_finished | alu_finished
        if len(finished) > 0:
            for op in finished:
                for next_op in op.next_nodes:
                    if next_op.ready(step):
                        if next_op.type == "mul":
                            mul_ready.add(next_op)
                        else:
                            alu_ready.add(next_op)
        mul_ready_list = list(mul_ready)
        alu_ready_list = list(alu_ready)
        mul_ready_list.sort(key=lambda x: x.priority, reverse=True)
        alu_ready_list.sort(key=lambda x: x.priority, reverse=True)

        """
        print ready_list
        """
        print "\nAt step", step, ":"
        if len(mul_ready_list) == 0:
            print "There is no MUL option ready."
        else:
            print "The ready MUL options:"
            for op in mul_ready_list:
                print("\tid: " + str(op.id) + " \ttype: " + op.type)

        if len(alu_ready_list) == 0:
            print "There is no ALU option ready."
        else:
            print "The ready ALU options:"
            for op in alu_ready_list:
                print("\tid: " + str(op.id) + " \ttype: " + op.type)

        """
        mul_schedule and alu_schedule at this step
        """
        mul_schedule = set()
        alu_schedule = set()
        if len(mul_ready_list) > 0:
            for op in mul_ready_list:
                if len(mul_schedule) + len(mul_unfinished) < capacity["mul"]:
                    mul_schedule.add(op)
                    op.set_step(step)

        if len(alu_ready_list) > 0:
            for op in alu_ready_list:
                if len(alu_schedule) + len(alu_unfinished) < capacity["alu"]:
                    alu_schedule.add(op)
                    op.set_step(step)

        """
        print mul_schedule and alu_schedule
        update unfinished sets 
        """
        if len(mul_schedule) == 0:
            print "There is no MUL option scheduled."
        else:
            print "The scheduled MUL options:"
            for op in mul_schedule:
                print("\tid: " + str(op.id) + " \ttype: " + op.type)
                mul_unfinished.add(op)

        if len(alu_schedule) == 0:
            print "There is no ALU option scheduled."
        else:
            print "The scheduled ALU options:"
            for op in alu_schedule:
                print("\tid: " + str(op.id) + " \ttype: " + op.type)
                alu_unfinished.add(op)

        ops_waiting.difference_update(mul_schedule)
        ops_waiting.difference_update(alu_schedule)

        step = step + 1


if __name__ == "__main__":
    main()