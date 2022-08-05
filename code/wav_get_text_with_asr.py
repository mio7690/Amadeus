import torch
import argparse
from transformers import AutoProcessor, AutoModelForCTC
import torchaudio
import os
import tqdm

class AmadeusDataset(torch.utils.data.Dataset):
  def __init__(self,wav_path):
        self.root = wav_path
        self.wav_files = [f for f in os.listdir(self.root) if f.endswith('.wav')]

  def __len__(self):
        return len(self.wav_files)

  def __getitem__(self, index):
        wav_file = self.wav_files[index]
        wav_path = os.path.join(self.root,wav_file)
        wav_data, sample_rate = torchaudio.load(wav_path, frame_offset=0 , num_frames=-1, normalize=True, channels_first=True)
        wav_data = wav_data.squeeze(0)
        return wav_data, wav_file

def process(args):
    wav_dataset = AmadeusDataset(args.wav_path)
    dataloader = torch.utils.data.DataLoader(wav_dataset, batch_size=args.batch_size, shuffle=False, num_workers=args.num_workers)

    print("Loading model...")
    processor = AutoProcessor.from_pretrained("thunninoi/wav2vec2-japanese-hiragana-vtuber")
    model = AutoModelForCTC.from_pretrained("thunninoi/wav2vec2-japanese-hiragana-vtuber")
    print("Model loaded")
    model.to(args.device)

    print("Start processing...")
    wav_paths = []
    wav_texts = []
    cnt = 0
    for batch in tqdm.tqdm(dataloader):
        cnt+=1
        if cnt>2:
            break
        wav_inputs,wav_files = batch
        wav_inputs = processor(wav_inputs,sampling_rate=16000,return_tensors="pt", padding=True)
        wav_inputs = wav_inputs.to(args.device)
        with torch.no_grad():
            logits = model(wav_inputs.input_values, attention_mask=wav_inputs.attention_mask).logits
        pred_ids = torch.argmax(logits, dim=-1)
        pred_string = processor.batch_decode(pred_ids)

        wav_paths.extend(wav_files)
        wav_texts.extend(pred_string)
    
    with open(args.output_path,'w') as f:
        for wav_path,wav_text in zip(wav_paths,wav_texts):
            f.write('wav/'+wav_path+'|'+wav_text+'\n')
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--wav_path",type=str,required=True)
    parser.add_argument("--output_path",type=str,required=True)
    parser.add_argument("--batch_size",type=int,default=32)
    parser.add_argument("--num_workers",type=int,default=4)
    parser.add_argument("--device",type=str,default="cpu")
    args = parser.parse_args()

    process(args)
