<script lang="ts">
  function handleSubmit(event: Event) {
    const form = event.target as HTMLFormElement;
    const fileInput = form.querySelector(
      'input[type="file"]'
    ) as HTMLInputElement;
    const file = fileInput.files?.[0];

    const anomalyElement = document.getElementById("anomaly")!;
    const goodnessElement = document.getElementById("goodness")!;

    if (file) {
      const formData = new FormData();
      formData.append("image", file);

      fetch("/benford", {
        method: "POST",
        body: formData,
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error("Network response was not ok");
          }
          return response.json();
        })
        .then((data) => {
          console.log("Success:", data);
          anomalyElement.textContent = `Anomaly detected: ${data.anomaly}`;
          goodnessElement.textContent = `Goodness of fit: ${data.goodness_of_fit}`;
        })
        .catch((error) => {
          console.error("Error:", error);
        });
    } else {
      console.error("No file selected");
    }
  }
</script>

<main>
  <h1>Image Anomaly Detection Platform (Proof of concept)</h1>
  <p>
    Since this is proof-of-concept only, only uncompressed images (BMP),
    lossless compressed images (PNG), and lossy compressed images (JPEG)
    (excluding JPEG2000) are supported.
  </p>

  <!-- Submission form -->
  <!-- svelte-ignore event_directive_deprecated -->
  <form on:submit|preventDefault={handleSubmit}>
    <label for="image">Upload an image:</label>
    <input
      type="file"
      id="image"
      name="image"
      accept="image/bmp, image/png, image/jpg, image/jpeg"
      required
    />
    <button type="submit">Submit</button>
  </form>

  <p id="anomaly"></p>
  <p id="goodness"></p>
</main>
