import os
from os.path import join as opj

import torchaudio
from tqdm import tqdm

downsample_rate = 16000

clean_train_path = "./data/DEMAND_VCTK/clean_trainset_wav"
noisy_train_path = "./data/DEMAND_VCTK/noisy_trainset_wav"

clean_test_path = "./data/DEMAND_VCTK/clean_testset_wav"
noisy_test_path = "./data/DEMAND_VCTK/noisy_testset_wav"

resample_path = "./data/DEMAND_VCTK_16k"


def downsample_wave(clean_path, noisy_path, sample_rate=downsample_rate, phase="train"):
    clean_list = os.listdir(clean_path)
    noisy_list = os.listdir(noisy_path)

    clean_list.sort()
    noisy_list.sort()

    clean_resample_path = opj(resample_path, "clean_" + phase)
    noisy_resample_path = opj(resample_path, "noisy_" + phase)

    if not os.path.isdir(clean_resample_path):
        os.makedirs(clean_resample_path)

    if not os.path.isdir(noisy_resample_path):
        os.makedirs(noisy_resample_path)

    tf = torchaudio.transforms.Resample(48000, sample_rate)

    for i in tqdm(range(len(clean_list))):
        clean, sr = torchaudio.load(opj(clean_path, clean_list[i]))
        noisy, sr = torchaudio.load(opj(noisy_path, noisy_list[i]))

        clean = tf(clean)
        noisy = tf(noisy)

        torchaudio.save(opj(clean_resample_path, clean_list[i]), clean, sample_rate)
        torchaudio.save(opj(noisy_resample_path, noisy_list[i]), noisy, sample_rate)


if __name__ == "__main__":
    print("--- Trainset Resampling ---")
    downsample_wave(
        clean_train_path, noisy_train_path, sample_rate=downsample_rate, phase="train"
    )
    print("--- Testset Resampling ---")
    downsample_wave(
        clean_test_path, noisy_test_path, sample_rate=downsample_rate, phase="test"
    )
