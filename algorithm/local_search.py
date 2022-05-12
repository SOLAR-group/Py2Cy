import random
import time
from abc import ABCMeta, abstractmethod
import timeit
from edit import TypeInsertion
from patch import Patch
from algorithm.algorithm import Algorithm


class LocalSearch(Algorithm):

    def get_neighbour(self, patch):

        patch.add(TypeInsertion.create(self.program))
        return patch

    def run(self, warmup_reps=5, epoch=1, max_iter=150):

        warmup = list()
        empty_patch = Patch(self.program)
        for i in range(warmup_reps):
            result = self.program.evaluate_patch(empty_patch)
            if result["status"] is "success":
                warmup.append(float(result["value"]))
        original_fitness = float(sum(warmup)) / len(warmup) if warmup else None

        result = []

        for cur_epoch in range(1, epoch + 1):
            best_patch = empty_patch
            best_fitness = original_fitness

            # Result Initilization
            result_list = {"success": 0, "compilation_fail": 0,
                           "bug_found": 0, "wrong_value": 0}

            start = time.time()
            for cur_iter in range(1, max_iter + 1):
                print(cur_iter)
                new_patch = self.get_neighbour(best_patch.clone())
                result = self.program.evaluate_patch(new_patch)
                print(result)
                result_list[result["status"]] += 1

                if result["status"] == "success":
                    value = float(result["value"])
                    if value < best_fitness:
                        best_fitness = value
                        best_patch = new_patch

                # if run.fitness is not None and self.stopping_criterion(cur_iter, run.fitness):
                #     cur_result['Success'] = True
                #     break

            total_time = time.time() - start

            self.program.write_result(best_patch)
            print("Best Fitness: " + str(best_fitness))
            print("Best Patch located in output/result.pyx")
            print("Total time taken: " + str(total_time))

        return result
