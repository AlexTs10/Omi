import io
import wave
from pyogg import OpusDecoder


# frames is 2darray
def create_wav_from_bytes(file_path: str, frames: [], codec: str, frame_rate: int = 16000, channels: int = 1, sample_width: int = 2):
    # opus
    if codec == "opus":
        # Create an Opus decoder
        opus_decoder = OpusDecoder()
        opus_decoder.set_channels(channels)
        opus_decoder.set_sampling_frequency(frame_rate)

        wave_write = wave.open(file_path, "wb")
        # Save the wav's specification
        wave_write.setnchannels(channels)
        wave_write.setframerate(frame_rate)
        wave_write.setsampwidth(sample_width)

        encoded_packets = []
        for frame in frames:
            encoded_packets.append(memoryview(bytearray(frame)))

        for encoded_packet in encoded_packets:
            decoded_pcm = opus_decoder.decode(encoded_packet)

            # Save the decoded PCM as a new wav file
            wave_write.writeframes(decoded_pcm)

        wave_write.close()

        return

    # pcm16
    if codec == "pcm16":
        wave_write = wave.open(file_path, "wb")
        # Save the wav's specification
        wave_write.setnchannels(channels)
        wave_write.setframerate(frame_rate)
        wave_write.setsampwidth(sample_width)

        for frame in frames:
            decoded_pcm = frame
            wave_write.writeframes(decoded_pcm)

        wave_write.close()
        return

    raise Exception(f"codec {codec} is not supported")
