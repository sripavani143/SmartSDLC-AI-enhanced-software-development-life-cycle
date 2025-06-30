from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from app import config

print("Using URL:", config.WATSONX_URL)
print("Using API Key:", config.WATSONX_API_KEY[:5], "***")
print("Using Project ID:", config.WATSONX_PROJECT_ID)


def query_watsonx(prompt: str) -> str:  # 🔁 Renamed from call_watsonx to query_watsonx
    credentials = {
        "apikey": config.WATSONX_API_KEY,
        "url": config.WATSONX_URL
    }

    mi = ModelInference(
        model_id=f"ibm/{config.WATSONX_MODEL_ID}",
        project_id=config.WATSONX_PROJECT_ID,
        credentials=credentials
    )

    params = {
        GenParams.DECODING_METHOD: "greedy",
        GenParams.MAX_NEW_TOKENS: 300,
        GenParams.MIN_NEW_TOKENS: 10,
        GenParams.TEMPERATURE: 0.5,
        GenParams.TOP_K: 50,
    }

    result = mi.generate_text(prompt=prompt, params=params)

    if isinstance(result, str):
        return result

    return result.get("results", [{}])[0].get("generated_text", "No output received.")
