from automat import MethodicalMachine
from enum import Enum
import random
import uuid


class State(Enum):
    STARTED = 'started'
    IN_PROCESS = 'in process'
    RESULT_RECEIVED = 'result received'
    FAILED = 'failed'
    COMPLETED = 'completed'
    CANCELED = 'canceled'


class MyMachine(object):
    _machine = MethodicalMachine()
    failures = 0

    def __init__(self):
        self.submissions = []
        self.results = []

    @_machine.state(initial=True, serialized=State.STARTED)
    def STARTED(self):
        pass
    
    @_machine.state(serialized=State.IN_PROCESS)
    def IN_PROCESS(self):
        pass

    @_machine.state(serialized=State.RESULT_RECEIVED)
    def RESULT_RECEIVED(self):
        pass

    @_machine.state(serialized=State.FAILED)
    def FAILED(self):
        pass

    @_machine.state(serialized=State.CANCELED)
    def CANCELED(self):
        pass

    @_machine.state(serialized=State.COMPLETED)
    def COMPLETED(self):
        pass

    @_machine.input()
    def submit(self, submission_id):
        pass

    @_machine.output()
    def _record_submission(self, submission_id):
        self.submissions.append(submission_id)

    @_machine.input()
    def fail(self):
        pass

    @_machine.input()
    def cancel(self):
        pass

    @_machine.output()
    def _record_failure(self):
        self.failures += 1
        if self.failures > 3:
            print('Canceling due to too many failures.')
            self.cancel()
            return 'canceled'
        else:
            print('Resubmitting.')
            self.submit(uuid.uuid4())

    @_machine.input()
    def process_result(self, result):
        pass

    @_machine.input()
    def pass_result(self, result):
        pass

    @_machine.output()
    def _qc_result(self, result):
        if result < 0.6:
            print('Failed QC!')
            self.fail()
        else:
            print('Passed QC!')
            self.pass_result(result)
            return 'passed'

    STARTED.upon(submit, enter=IN_PROCESS, outputs=[_record_submission])
    IN_PROCESS.upon(submit, enter=IN_PROCESS, outputs=[_record_submission])
    IN_PROCESS.upon(cancel, enter=CANCELED, outputs=[])
    IN_PROCESS.upon(fail, enter=IN_PROCESS, outputs=[_record_failure])
    IN_PROCESS.upon(process_result, enter=IN_PROCESS, outputs=[_qc_result])
    IN_PROCESS.upon(pass_result, enter=COMPLETED, outputs=[])


class AnotherMachine(object):
    _machine = MethodicalMachine()
    @_machine.state(initial=True)
    def state1(self):
        pass
    @_machine.state()
    def state2(self):
        pass
    @_machine.state()
    def state3(self):
        pass
    @_machine.input()
    def input1(self):
        pass
    @_machine.input()
    def input2(self):
        pass
    @_machine.input()
    def input3(self):
        pass

    @_machine.output()
    def _move_to_state2(self):
        print('called2')
        self.input2()
    @_machine.output()
    def on_state3(self):
        print('called3')

    state1.upon(input1, enter=state2, outputs=[_move_to_state2])
    state2.upon(input2, enter=state3, outputs=[on_state3])


if __name__ == '__main__':
    machine = AnotherMachine()
    machine.input1()
    if False:
        # Broken, see https://github.com/glyph/automat/issues/72
        import uuid, random
        for i in range(10):
            print('Run %s' % i)
            machine = MyMachine()
            results = []
            while not ({'canceled', 'passed'} & set(results)):
                machine.submit(uuid.uuid4())
                result = random.random()
                results = machine.process_result(result)
                print(results)