### Pretrain
 
1. 将 bert-base-uncased.zip、annotations.zip、pos_tag.json和模型文件model_base_14M.pth 置于./
2. 修改预训练配置文件configs/pretrain.yaml中的train_file字段为包含coco.json和vg.json所在路径的列表
3. 将coco和vg的图片放在./pretrain_data/vl_pair文件夹下，结构如图
 <img src="https://github.com/LHL3341/Adapter-BLIP/blob/main/README.assets/image-20230905205831636.png" alt="image-20230905205919235" style="zoom:50%;" />
4. 运行代码

```
unzip bert-base-uncased.zip
unzip annotations.zip
bash run.sh
```

### Finetune
1. 下载imagecode数据集

   图片：[image-sets.zip · BennoKrojer/ImageCoDe at main (huggingface.co)](https://huggingface.co/datasets/BennoKrojer/ImageCoDe/blob/main/image-sets.zip)

   标注：[imagecode/data at main · McGill-NLP/imagecode (github.com)](https://github.com/McGill-NLP/imagecode/tree/main/data)目录下的3个json文件，分别为训练、验证和测试集

2. ```bash
   mkdir data
   mv image-sets.zip dataset/
   mv train_data.json dataset/
   mv valid_data.json dataset/
   mv test_data_unlabeled.json dataset/
   cd dataset
   unzip image-sets.zip #若unzip无法解压大文件，可用7z解压或将数据集先转为tar.gz格式
   ```

   

3. 检查图片路径为./dataset/image-sets，标注路径为./dataset，如图所示<img src="https://github.com/LHL3341/Adapter-BLIP/blob/main/README.assets/image-20230907165345041.png" alt="image-20230905205919235" style="zoom:50%;" />

4. ```bash
   nohup python -u finetune.py --finetuned_checkpoint_path {预训练模型路径} > finetune.log 2>&1 & #开始训练
   ```

### Zero-Shot
```bash
python zero-shot.py --finetuned_checkpoint_path {预训练模型路径}
```

### Analysis
```bash
python analysis/analysis_finetune.py --finetuned_checkpoint_path {预训练模型路径} #评估finetune模型
```

### Ablation Study
消融实验中，通过调整命令行参数调整图像掩码率和文本prompt长度
```bash
#img_mask_rate={图片掩码率}
#prompt_length={文本prompt长度}
nohup python -u -m torch.distributed.run --nproc_per_node 4 main.py --mask_rate ${img_mask_rate} --prompt_length ${prompt_length} --output_dir 'output/Pretrain/'$img_mask_rate'_'$prompt_length'' > pretrain.log 2>&1 &
```   
### COCO-5k
修改./configs/retrieval_coco.yaml中的pretrained字段为待测试检查点的路径
```bash
python train_retrieval.py --config configs/retrieval_coco.yaml --output_dir 'output/Retrieval_coco'
```
### Flickr30k-1k
将flickr30k-images文件夹置于./pretrain_data下
修改./configs/retrieval_flickr.yaml中的pretrained字段为待测试检查点的路径
```bash
python train_retrieval.py --config configs/retrieval_flickr.yaml --output_dir 'output/Retrieval_flickr'
```