import { generateEmbeddings } from "../src/embedding.js";

const chunks = [
  "Hypertension is a chronic medical condition characterized by high blood pressure.",
  "Common symptoms of hypertension may include headache and dizziness.",
  "Treatment includes lifestyle changes and medications."
];

const vectors = await generateEmbeddings(chunks);

console.log("Number of chunks:", chunks.length);
console.log("Number of vectors:", vectors.length);

if (chunks.length === vectors.length) {
  console.log("Document embedding test passed ✅");
} else {
  console.log("Document embedding test failed ❌");
}