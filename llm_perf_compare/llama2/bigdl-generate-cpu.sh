source "/home/intel/miniconda3/etc/profile.d/conda.sh"
conda activate llm

python3 bigdl-generate-cpu.py \
        --repo-id-or-model-path /home/intel/PAE/6.Max/git/AI_Samples/llama2/llama-2-7b-chat-hf \
	--n-predict 256
