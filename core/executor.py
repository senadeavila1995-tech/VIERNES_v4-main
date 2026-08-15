from time import perf_counter

from agents.memory_agent import MemoryAgent
from models.action_result import ActionResult


class Executor:
    """
    Ejecuta un Plan paso a paso utilizando el Router.
    """

    def __init__(self):

        self.memory = MemoryAgent()
        self.history = []


    # =====================================================
    # EJECUTAR PLAN
    # =====================================================

    def execute(self, router, plan):

        total = len(plan.steps)


        if total == 0:

            return ActionResult(

                success=True,

                message="No hay tareas para ejecutar."

            )


        print(f"\n🚀 Ejecutando plan ({total} pasos)\n")


        self.history.clear()


        start_plan = perf_counter()


        results = []


        for index, step in enumerate(plan.steps, start=1):

            print(
                f"[{index}/{total}] ⚙ {step.action}"
            )


            start = perf_counter()


            try:

                result = router.dispatch_step(
                    step
                )


                elapsed = perf_counter() - start


                print(
                    f"✅ {step.action} ({elapsed:.2f}s)"
                )


                self.history.append({

                    "step": step,

                    "success": True,

                    "elapsed": elapsed,

                    "result": result

                })


                results.append(result)


            except Exception as e:


                elapsed = perf_counter() - start


                print(
                    f"❌ {step.action} ({elapsed:.2f}s)"
                )


                print(e)


                self.history.append({

                    "step": step,

                    "success": False,

                    "elapsed": elapsed,

                    "error": str(e)

                })


                return ActionResult(

                    success=False,

                    message=f"Error ejecutando '{step.action}'.",

                    error=str(e)

                )


        total_time = perf_counter() - start_plan


        print(
            f"\n🏁 Plan finalizado en {total_time:.2f}s"
        )


        return ActionResult(

            success=True,

            message="Plan ejecutado correctamente.",

            data=results

        )


    # =====================================================
    # HISTORIAL
    # =====================================================

    def get_history(self):

        return self.history


    def clear_history(self):

        self.history.clear()


    # =====================================================
    # ESTADÍSTICAS
    # =====================================================

    def statistics(self):

        success = 0

        failed = 0

        elapsed = 0


        for item in self.history:

            elapsed += item["elapsed"]


            if item["success"]:

                success += 1

            else:

                failed += 1


        return {

            "steps": len(self.history),

            "success": success,

            "failed": failed,

            "time": round(elapsed, 2)

        }