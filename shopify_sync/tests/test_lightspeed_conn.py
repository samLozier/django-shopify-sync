from lightspeed_app.lightspeed_conn import ProcessManager


class TestProcessManager:
    def test_minimal_process_manager_constructor(self):
        """
        Minimal test of process creation
        :return:
        :rtype:
        """
        assert ProcessManager(
            endpoint="/item", action_type="GET", expected_resp_obj_type="Item"
        )

    def test_builder(self):
        assert False
