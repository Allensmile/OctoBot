import logging
import threading

from config.cst import *
from evaluator.evaluator import Evaluator
from evaluator.evaluator_matrix import EvaluatorMatrix
from evaluator.social_evaluator_not_threaded_update import SocialEvaluatorNotThreadedUpdateThread
from evaluator.time_frame_update import TimeFrameUpdateDataThread


class EvaluatorThread(threading.Thread):
    def __init__(self, config, symbol, time_frame, exchange, notifier, trader, social_eval_list):
        threading.Thread.__init__(self)
        self.config = config
        self.exchange = exchange
        self.exchange_time_frame = self.exchange.get_time_frame_enum()
        self.symbol = symbol
        self.time_frame = time_frame
        self.notifier = notifier
        self.trader = trader

        self.matrix = EvaluatorMatrix()

        self.thread_name = "TA THREAD - " + self.symbol \
                           + " - " + self.exchange.__class__.__name__ \
                           + " - " + str(self.time_frame)
        self.logger = logging.getLogger(self.thread_name)

        # Create Evaluator
        self.evaluator = Evaluator()
        self.evaluator.set_config(self.config)
        self.evaluator.set_symbol(self.symbol)
        self.evaluator.set_time_frame(self.time_frame)
        self.evaluator.set_notifier(self.notifier)
        self.evaluator.set_trader(self.trader)
        self.evaluator.set_social_eval(social_eval_list, self)

        # Create refreshing threads
        self.data_refresher = TimeFrameUpdateDataThread(self)
        self.social_evaluator_refresh = SocialEvaluatorNotThreadedUpdateThread(self)

    def notify(self, notifier_name):
        if self.data_refresher.get_refreshed_times() > 0:
            self.logger.debug("Notified by " + notifier_name)
            self.refresh_eval(notifier_name)
        else:
            self.logger.debug("Notification by " + notifier_name + " ignored")

    def refresh_eval(self, ignored_evaluator=None):
        # First eval --> create_instances
        # Instances will be created only if they don't already exist
        self.evaluator.create_ta_eval()

        # update eval
        self.evaluator.update_ta_eval(ignored_evaluator)

        # for Debug purpose
        ta_eval_list_result = []
        for ta_eval in self.evaluator.get_ta_eval_list():
            result = ta_eval.get_eval_note()
            ta_eval_list_result.append(result)
            self.matrix.set_eval(EvaluatorMatrixTypes.TA, ta_eval.__class__.__name__, result)

        self.logger.debug("TA EVAL : " + str(ta_eval_list_result))

        social_eval_list_result = []
        for social_eval in self.evaluator.get_social_eval_list():
            result = social_eval.get_eval_note()
            social_eval_list_result.append(result)
            self.matrix.set_eval(EvaluatorMatrixTypes.SOCIAL, social_eval.__class__.__name__, result)

        self.logger.debug("Social EVAL : " + str(social_eval_list_result))

        # calculate the final result
        self.evaluator.finalize()
        self.logger.debug("FINAL : " + str(self.evaluator.get_state()))
        self.logger.debug("MATRIX : " + str(self.matrix.get_matrix()))

    def run(self):
        # Start refresh threads
        self.data_refresher.start()
        self.social_evaluator_refresh.start()
        self.data_refresher.join()
        self.social_evaluator_refresh.join()
