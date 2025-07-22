## 🧠 Model Issues

### Tensor Shape Errors
**Problem:** `RuntimeError: mat1 and mat2 shapes cannot be multiplied`

**Debug approach:**
```python
# Always debug with shapes
print(f"Query shape: {query.shape}")
print(f"Key shape: {key.shape}")
print(f"Value shape: {value.shape}")

# Common fix for attention
scores = torch.matmul(query, key.transpose(-2, -1))