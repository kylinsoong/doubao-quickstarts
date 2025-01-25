import uvloop
import os
from bytedance_ark_batch_inference.client import BatchInferenceClient
from bytedance_tos.tos_client import TosClient


async def main():
    tos_client = TosClient()
    batch_inference_client = BatchInferenceClient()


    # put object
    bucket_name = os.environ.get("TOS_JSONL_BUCKET")
    object_key = os.environ.get("TOS_JSONL_BUCKET_KEY")

    # create batch job
    # output key should be existed
    output_key = os.environ.get("TOS_BATCH_INFERENCE_OUTPUT")
    response = await batch_inference_client.create_batch_inference_job(bucket_name, object_key, output_key)
    response = await batch_inference_client.ListBatchInferenceJobs(['Running'])

    print('done')

if __name__ == '__main__':
    uvloop.run(main())
