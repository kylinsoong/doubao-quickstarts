import uvloop
import os
from inference import BatchInferenceClient


async def main():
    input_bucket_name = os.environ.get("TOS_JSONL_BUCKET")
    object_key = os.environ.get("TOS_JSONL_BUCKET_KEY")
    output_bucket_name = os.environ.get("TOS_BATCH_INFERENCE_BUCKET")
    output_key = os.environ.get("TOS_BATCH_INFERENCE_OUTPUT")

    response = await create_batch_inference_job(input_bucket_name,output_bucket_name, object_key, output_key)
    response = await ListBatchInferenceJobs(['Running'])

    print('done')

if __name__ == '__main__':
    uvloop.run(main())
