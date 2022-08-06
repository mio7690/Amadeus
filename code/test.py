import torch
import torchaudio
import librosa
from datasets import load_dataset
import MeCab
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
import re
# config
wakati = MeCab.Tagger("-Owakati")
chars_to_ignore_regex = '[\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\,\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\、\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\。\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\．\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\「\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\」\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\…\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\？\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\・]'
kakasi = pykakasi.kakasi()
kakasi.setMode("J","H")
kakasi.setMode("K","H")
kakasi.setMode("r","Hepburn")
conv = kakasi.getConverter()
# load data, processor and model
test_dataset = load_dataset("common_voice", "ja", split="test[:2%]")
processor = Wav2Vec2Processor.from_pretrained("vumichien/wav2vec2-large-xlsr-japanese-hỉragana")
model = Wav2Vec2ForCTC.from_pretrained("vumichien/wav2vec2-large-xlsr-japanese-hỉragana")
resampler = lambda sr, y: librosa.resample(y.numpy().squeeze(), sr, 16_000)
# Preprocessing the datasets.
def speech_file_to_array_fn(batch):
    batch["sentence"] = conv.do(wakati.parse(batch["sentence"]).strip())
    batch["sentence"] = re.sub(chars_to_ignore_regex,'', batch["sentence"]).strip()
    speech_array, sampling_rate = torchaudio.load(batch["path"])
    batch["speech"] = resampler(sampling_rate, speech_array).squeeze()
    return batch
test_dataset = test_dataset.map(speech_file_to_array_fn)
import ipdb;ipdb.set_trace()
inputs = processor(test_dataset["speech"][:2], sampling_rate=16_000, return_tensors="pt", padding=True)
with torch.no_grad():
    logits = model(inputs.input_values, attention_mask=inputs.attention_mask).logits
predicted_ids = torch.argmax(logits, dim=-1)
print("Prediction:", processor.batch_decode(predicted_ids))
print("Reference:", test_dataset["sentence"][:2])
