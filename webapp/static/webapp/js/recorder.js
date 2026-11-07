(function () {
    "use strict";

    const TARGET_RATE = 16000;

    function mergeChunks(chunks) {
        const length = chunks.reduce((sum, c) => sum + c.length, 0);
        const result = new Float32Array(length);
        let offset = 0;
        for (const chunk of chunks) {
            result.set(chunk, offset);
            offset += chunk.length;
        }
        return result;
    }

    function downsample(samples, inputRate, outputRate) {
        if (outputRate >= inputRate) return samples;
        const ratio = inputRate / outputRate;
        const result = new Float32Array(Math.floor(samples.length / ratio));
        for (let i = 0; i < result.length; i++) {
            const start = Math.floor(i * ratio);
            const end = Math.min(Math.floor((i + 1) * ratio), samples.length);
            let sum = 0;
            for (let j = start; j < end; j++) sum += samples[j];
            result[i] = sum / Math.max(end - start, 1);
        }
        return result;
    }

    function encodeWav(samples, sampleRate) {
        const buffer = new ArrayBuffer(44 + samples.length * 2);
        const view = new DataView(buffer);
        const writeString = (offset, text) => {
            for (let i = 0; i < text.length; i++) view.setUint8(offset + i, text.charCodeAt(i));
        };
        writeString(0, "RIFF");
        view.setUint32(4, 36 + samples.length * 2, true);
        writeString(8, "WAVE");
        writeString(12, "fmt ");
        view.setUint32(16, 16, true);
        view.setUint16(20, 1, true);
        view.setUint16(22, 1, true);
        view.setUint32(24, sampleRate, true);
        view.setUint32(28, sampleRate * 2, true);
        view.setUint16(32, 2, true);
        view.setUint16(34, 16, true);
        writeString(36, "data");
        view.setUint32(40, samples.length * 2, true);
        for (let i = 0; i < samples.length; i++) {
            const s = Math.max(-1, Math.min(1, samples[i]));
            view.setInt16(44 + i * 2, s < 0 ? s * 0x8000 : s * 0x7fff, true);
        }
        return new Blob([view], {type: "audio/wav"});
    }

    class WavRecorder {
        async start() {
            this.stream = await navigator.mediaDevices.getUserMedia({audio: true});
            this.context = new AudioContext();
            this.source = this.context.createMediaStreamSource(this.stream);
            this.processor = this.context.createScriptProcessor(4096, 1, 1);
            this.chunks = [];
            this.processor.onaudioprocess = (e) => {
                this.chunks.push(new Float32Array(e.inputBuffer.getChannelData(0)));
            };
            this.source.connect(this.processor);
            this.processor.connect(this.context.destination);
        }

        async stop() {
            this.processor.disconnect();
            this.source.disconnect();
            this.stream.getTracks().forEach((track) => track.stop());
            const inputRate = this.context.sampleRate;
            await this.context.close();
            return encodeWav(downsample(mergeChunks(this.chunks), inputRate, TARGET_RATE), TARGET_RATE);
        }
    }

    function setupForm(form) {
        const button = form.querySelector("[data-record-button]");
        const label = form.querySelector("[data-record-label]");
        const status = form.querySelector("[data-record-status]");
        const input = form.querySelector("input[name=audio]");
        let recorder = null;

        button.addEventListener("click", async () => {
            if (!recorder) {
                if (!form.reportValidity()) return;
                if (!navigator.mediaDevices || !window.AudioContext) {
                    status.textContent = "Audio recording is not supported by this browser.";
                    return;
                }
                try {
                    recorder = new WavRecorder();
                    await recorder.start();
                } catch (err) {
                    recorder = null;
                    status.textContent = `Microphone not available (${err.message}).`;
                    return;
                }
                label.textContent = "Stop";
                button.classList.replace("btn-outline-danger", "btn-danger");
                status.textContent = "Recording... click Stop when you have finished speaking.";
                return;
            }

            const blob = await recorder.stop();
            recorder = null;
            const transfer = new DataTransfer();
            transfer.items.add(new File([blob], "recording.wav", {type: "audio/wav"}));
            input.files = transfer.files;
            button.disabled = true;
            label.textContent = "Analyzing...";
            status.textContent = "";
            form.submit();
        });
    }

    document.querySelectorAll("form[data-recorder]").forEach(setupForm);
})();
