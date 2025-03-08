#from maa.agent.agent_server import AgentServer
from maa.context import Context
from maa.custom_action import CustomAction
import time

#@AgentServer.custom_action("ShotSelf")
class ShotSelf(CustomAction):
    def run(
        self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult:
        image = context.tasker.controller.post_screencap().wait().get()
        item = context.run_recognition("展开道具", image)
        if item:
            x, y = (
                item.best_result.box[0] + item.best_result.box[2] // 2,
                item.best_result.box[1] + item.best_result.box[3] // 2,
            )
            context.tasker.controller.post_click(x, y).wait()
            time.sleep(1)
            image = context.tasker.controller.post_screencap().wait().get()
        health = context.run_recognition("生命值缺失", image)
        health_gem = context.run_recognition("检查活力宝石", image)
        if health and health_gem:
            x, y = (
                health_gem.best_result.box[0] + health_gem.best_result.box[2] // 2,
                health_gem.best_result.box[1] + health_gem.best_result.box[3] // 2,
            )
            context.tasker.controller.post_click(x, y).wait()
            time.sleep(1)
            context.run_task("使用道具")
            time.sleep(1)
            image = context.tasker.controller.post_screencap().wait().get()
        lock = context.run_recognition("检查手铐", image)
        lock_status = context.run_recognition("检查手铐状态", image)
        if lock and not (lock_status):
            x, y = (
                lock.best_result.box[0] + lock.best_result.box[2] // 2,
                lock.best_result.box[1] + lock.best_result.box[3] // 2,
            )
            context.tasker.controller.post_click(x, y).wait()
            time.sleep(1)
            context.run_task("使用道具")
            time.sleep(1)
            image = context.tasker.controller.post_screencap().wait().get()
        reversal = context.run_recognition("检查逆转魔术", image)
        if reversal:
            x, y = (
                reversal.best_result.box[0] + reversal.best_result.box[2] // 2,
                reversal.best_result.box[1] + reversal.best_result.box[3] // 2,
            )
            context.tasker.controller.post_click(x, y).wait()
            time.sleep(1)
            context.run_task("使用道具")
            time.sleep(1)
            barrel = context.run_recognition("检查枪管", image)
            if barrel:
                x, y = (
                    barrel.best_result.box[0] + barrel.best_result.box[2] // 2,
                    barrel.best_result.box[1] + barrel.best_result.box[3] // 2,
                )
                context.tasker.controller.post_click(x, y).wait()
                time.sleep(1)
                context.run_task("使用道具")
                time.sleep(1)
            context.run_task("向对方开枪")
            return CustomAction.RunResult(success=True)
        context.run_task("向自己开枪")
        return CustomAction.RunResult(success=True)
