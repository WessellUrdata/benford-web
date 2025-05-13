<script lang="ts">
  function handleSubmit(event: Event) {
    console.log("Button clicked");

    const form = event.target as HTMLFormElement;
    const fileInput = form.querySelector(
      'input[type="file"]'
    ) as HTMLInputElement;
    const file = fileInput.files?.[0];

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
</main>

<!-- <style>
  .logo {
    height: 6em;
    padding: 1.5em;
    will-change: filter;
    transition: filter 300ms;
  }
  .logo:hover {
    filter: drop-shadow(0 0 2em #646cffaa);
  }
  .logo.svelte:hover {
    filter: drop-shadow(0 0 2em #ff3e00aa);
  }
  .read-the-docs {
    color: #888;
  }
</style> -->
