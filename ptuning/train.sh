#!/bin/bash
PRE_SEQ_LEN=128
LR=2e-2
NUM_GPUS=2

torchrun --standalone --nnodes 1 --nproc_per_node $NUM_GPUS main.py \
    --do_train \
    --train_file data/role_data/train.json \
    --validation_file data/role_data/test.json \
    --preprocessing_num_workers 10 \
    --prompt_column prompt \
    --response_column response \
    --overwrite_cache \
    --model_name_or_path /data/zhimin/ChatGLM2-6B/model/chatglm2-6b \
    --output_dir output/cjz-roleglm-$PRE_SEQ_LEN-$LR \
    --overwrite_output_dir \
    --max_source_length 512 \
    --max_target_length 128 \
    --per_device_train_batch_size 1 \
    --per_device_eval_batch_size 1 \
    --gradient_accumulation_steps 16 \
    --predict_with_generate \
    --max_steps 3000 \
    --logging_steps 10 \
    --save_steps 1000 \
    --learning_rate $LR \
    --pre_seq_len $PRE_SEQ_LEN \
    --quantization_bit 4

