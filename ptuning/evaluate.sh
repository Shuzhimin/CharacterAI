PRE_SEQ_LEN=128
CHECKPOINT=cjz-roleglm-128-2e-2
STEP=3000
NUM_GPUS=2

torchrun --standalone --nnodes 1 --nproc_per_node $NUM_GPUS main.py \
    --do_predict \
    --validation_file /data/zhimin/ChatGLM2-6B/ptuning/data/role_data/test.json \
    --test_file /data/zhimin/ChatGLM2-6B/ptuning/data/role_data/test.json \
    --overwrite_cache \
    --prompt_column prompt \
    --response_column response \
    --model_name_or_path /data/zhimin/ChatGLM2-6B/model/chatglm2-6b \
    --ptuning_checkpoint ./output/$CHECKPOINT/checkpoint-$STEP \
    --output_dir ./output/$CHECKPOINT/result \
    --overwrite_output_dir \
    --max_source_length 512 \
    --max_target_length 128 \
    --per_device_eval_batch_size 1 \
    --predict_with_generate \
    --pre_seq_len $PRE_SEQ_LEN \
    --quantization_bit 4
