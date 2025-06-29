# Copyright (c) 2024-2025 MAA_SnowBreak
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
MAA_SnowBreak
MAA_SnowBreak 蜃梦笔谈地图判断程序
作者:Ostwind23
"""

from maa.context import Context
from maa.custom_action import CustomAction

import time


# @AgentServer.custom_action("StoryRogue")
class StoryRogue(CustomAction):
    # 静态计数器，记录成功运行的次数
    run_counter = 0

    def run(
        self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult:
        # 获取屏幕截图
        image = context.tasker.controller.post_screencap().wait().get()

        # 场景识别，分为走廊、红走廊、大门、庭院
        corridor_result = context.run_recognition("走廊场景识别", image)

        red_corridor_result = context.run_recognition("红走廊场景识别", image)

        gate_result = context.run_recognition("大门场景识别", image)

        courtyard_result = context.run_recognition("庭院场景识别", image)

        # 根据识别结果执行不同的操作
        if corridor_result:
            print("识别到走廊场景")
            # 走廊场景的处理逻辑
            return self.handle_corridor(context)
        elif red_corridor_result:
            print("识别到红走廊场景")
            # 红走廊场景的处理逻辑
            return self.handle_red_corridor(context)
        elif gate_result:
            print("识别到大门场景")
            # 大门场景的处理逻辑
            return self.handle_gate(context)
        elif courtyard_result:
            print("识别到庭院场景")
            # 庭院场景的处理逻辑
            return self.handle_courtyard(context)
        else:
            print("无法识别当前场景")
            # 默认处理或错误处理
            return CustomAction.RunResult(success=True)

    def handle_corridor(self, context: Context) -> CustomAction.RunResult:
        """走廊场景的处理逻辑"""
        print("执行走廊场景处理")
        # 前进7秒
        self.move_forward(context, 7)

        # 循环执行技能直到战斗结束
        # result = self.skill_cycle_until_exit(context)
        # 取消python中的战斗程序,移交至pipeline中

        return CustomAction.RunResult(success=True)

    def handle_red_corridor(self, context: Context) -> CustomAction.RunResult:
        """红走廊场景的处理逻辑"""
        print("执行红走廊场景处理")
        # 前进7秒
        self.move_forward(context, 7)
        # 循环执行技能直到战斗结束
        # result = self.skill_cycle_until_exit(context)
        # 取消python中的战斗程序,移交至pipeline中

        return CustomAction.RunResult(success=True)

    def handle_gate(self, context: Context) -> CustomAction.RunResult:
        """大门场景的处理逻辑"""
        print("执行大门场景处理")

        # 前进6秒
        self.move_forward(context, 6)

        # 向右移动3.5秒
        self.move_right(context, 3.5)

        # 循环执行技能直到战斗结束
        # result = self.skill_cycle_until_exit(context)
        # 取消python中的战斗程序,移交至pipeline中

        return CustomAction.RunResult(success=True)

    def handle_courtyard(self, context: Context) -> CustomAction.RunResult:
        """庭院场景的处理逻辑"""
        print("执行庭院场景处理")

        # 前进7.5秒
        self.move_forward(context, 7.5)

        # 屏幕从右往左滑动
        self.swipe_screen(context, 688, 316, 536, 316)

        # 循环执行技能直到战斗结束
        # result = self.skill_cycle_until_exit(context)
        # 取消python中的战斗程序,移交至pipeline中

        return CustomAction.RunResult(success=True)

    def move_forward(self, context: Context, duration: float) -> None:
        """持续前进指定秒数"""
        print(f"前进 {duration} 秒")
        x, y = 268, 423  # 前进按钮的坐标

        # 修复：确保转换为整数
        duration_ms = int(duration * 1000)
        # 使用长时间的swipe来模拟长按效果(起点和终点相同)
        context.tasker.controller.post_swipe(x, y, x, y, duration_ms).wait()
        time.sleep(0.5)  # 短暂等待以确保操作完成

    def move_right(self, context: Context, duration: float) -> None:
        """持续向右移动指定秒数"""
        print(f"向右移动 {duration} 秒")
        x, y = 370, 531  # 右进按钮的坐标

        # 修复：确保转换为整数
        duration_ms = int(duration * 1000)
        # 使用长时间的swipe来模拟长按效果(起点和终点相同)
        context.tasker.controller.post_swipe(x, y, x, y, duration_ms).wait()
        time.sleep(0.5)  # 短暂等待以确保操作完成

    def swipe_screen(
        self, context: Context, start_x: int, start_y: int, end_x: int, end_y: int
    ) -> None:
        """从一点滑动到另一点"""
        print(f"滑动屏幕 从 ({start_x}, {start_y}) 到 ({end_x}, {end_y})")
        context.tasker.controller.post_swipe(start_x, start_y, end_x, end_y, 500).wait()
        time.sleep(0.5)

    def use_e_skill(self, context: Context) -> None:
        """使用E技能"""
        print("使用E技能")
        context.tasker.controller.post_click(1042, 327).wait()
        time.sleep(3)  # 等待3秒再执行下一个动作

    def use_q_skill(self, context: Context) -> None:
        """使用Q技能"""
        print("使用Q技能")
        context.tasker.controller.post_click(1165, 329).wait()
        time.sleep(3)  # 等待3秒再执行下一个动作

    def check_battle_exit(self, context: Context) -> bool:
        """检查是否有退出按钮"""
        image = context.tasker.controller.post_screencap().wait().get()
        exit_result = context.run_recognition("检查退出按钮", image)
        return bool(exit_result)

    def skill_cycle_until_exit(self, context: Context) -> CustomAction.RunResult:
        """循环执行技能直到战斗结束"""
        print("开始循环执行技能")

        max_cycles = 8  # 防止无限循环的安全措施
        cycle_count = 0

        while cycle_count < max_cycles:
            # 检查是否有退出按钮
            if self.check_battle_exit(context):
                print("检测到战斗结束，点击退出")
                # 增加计数器并打印
                StoryRogue.run_counter += 1
                print(f"StoryRogue 程序运行次数: {StoryRogue.run_counter}")
                # 使用带错误处理的点击方式
                try:
                    context.tasker.controller.post_click(637, 637).wait()
                    time.sleep(2)
                    return CustomAction.RunResult(success=True)
                except Exception as e:
                    print(f"点击退出按钮时出错: {e}")
                    return CustomAction.RunResult(success=True)

            # 按E技能3次
            for _ in range(3):
                self.use_e_skill(context)

                # 每次技能后检查是否结束
                if self.check_battle_exit(context):
                    print("检测到战斗结束，点击退出")
                    # 增加计数器并打印
                    StoryRogue.run_counter += 1
                    print(f"StoryRogue 程序运行次数: {StoryRogue.run_counter}")
                    context.tasker.controller.post_click(637, 637).wait()
                    time.sleep(2)
                    return CustomAction.RunResult(success=True)

            # 按Q技能1次
            self.use_q_skill(context)

            cycle_count += 1
            print(f"完成技能循环 {cycle_count}/{max_cycles}")

        # 如果达到最大循环次数仍未结束
        print("达到最大循环次数，强制结束")
        return CustomAction.RunResult(success=True)
