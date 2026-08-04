import json
from teach_ai.envs import BASE_DIR


def dump_response(response, fn_o: str):
    fn_o = BASE_DIR / fn_o
    with open(fn_o, mode="w") as fp:
        json.dump(response.model_dump(), fp, indent=2, ensure_ascii=False)
    print(f"dumped: {fn_o}")
