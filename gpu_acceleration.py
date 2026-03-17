"""
GPU Acceleration Module for MindTrace
CuPy and CUDA-based high-performance computing
"""
import numpy as np
from typing import Optional, Tuple, List
import warnings

try:
    import cupy as cp
    GPU_AVAILABLE = True
except ImportError:
    GPU_AVAILABLE = False
    cp = None
    warnings.warn("CuPy not available. Using NumPy fallback.")


class GPUAccelerator:
    def __init__(self, device: int = 0):
        self.device = device
        self.gpu_available = GPU_AVAILABLE
        
        if self.gpu_available:
            cp.cuda.Device(device).use()
    
    def to_gpu(self, array: np.ndarray) -> "cp.ndarray":
        if not self.gpu_available:
            return array
        return cp.asarray(array)
    
    def to_cpu(self, gpu_array: "cp.ndarray") -> np.ndarray:
        if not self.gpu_available:
            return gpu_array
        return cp.asnumpy(gpu_array)
    
    def compute_similarities(self, embeddings1: np.ndarray, embeddings2: np.ndarray) -> np.ndarray:
        if self.gpu_available:
            e1 = self.to_gpu(embeddings1)
            e2 = self.to_gpu(embeddings2)
            
            normalized1 = e1 / cp.linalg.norm(e1, axis=1, keepdims=True)
            normalized2 = e2 / cp.linalg.norm(e2, axis=1, keepdims=True)
            
            similarities = cp.dot(normalized1, normalized2.T)
            return self.to_cpu(similarities)
        
        norm1 = embeddings1 / np.linalg.norm(embeddings1, axis=1, keepdims=True)
        norm2 = embeddings2 / np.linalg.norm(embeddings2, axis=1, keepdims=True)
        return np.dot(norm1, norm2.T)
    
    def batch_compute_embeddings(
        self,
        texts: List[str],
        embedding_fn
    ) -> np.ndarray:
        batch_size = 32
        all_embeddings = []
        
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            embeddings = embedding_fn(batch)
            
            if self.gpu_available:
                embeddings = self.to_gpu(embeddings)
            
            all_embeddings.append(embeddings)
        
        if self.gpu_available:
            return cp.vstack(all_embeddings)
        return np.vstack(all_embeddings)
    
    def matrix_multiplication(
        self,
        a: np.ndarray,
        b: np.ndarray,
        trans_a: bool = False,
        trans_b: bool = False
    ) -> np.ndarray:
        if self.gpu_available:
            a_gpu = self.to_gpu(a)
            b_gpu = self.to_gpu(b)
            
            if trans_a:
                a_gpu = a_gpu.T
            if trans_b:
                b_gpu = b_gpu.T
            
            result = cp.dot(a_gpu, b_gpu)
            return self.to_cpu(result)
        
        if trans_a:
            a = a.T
        if trans_b:
            b = b.T
        return np.dot(a, b)
    
    def singular_value_decomposition(
        self,
        matrix: np.ndarray,
        k: int = 10
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        if self.gpu_available:
            m = self.to_gpu(matrix)
            u, s, vt = cp.linalg.svd(m, full_matrices=False)
            return (
                self.to_cpu(u[:, :k]),
                self.to_cpu(s[:k]),
                self.to_cpu(vt[:k, :])
            )
        
        u, s, vt = np.linalg.svd(matrix, full_matrices=False)
        return u[:, :k], s[:k], vt[:k, :]
    
    def kmeans_gpu(
        self,
        data: np.ndarray,
        k: int,
        max_iter: int = 100,
        tol: float = 1e-4
    ) -> Tuple[np.ndarray, np.ndarray]:
        n_samples, n_features = data.shape
        
        if self.gpu_available:
            data = self.to_gpu(data)
            
            indices = cp.random.choice(n_samples, k, replace=False)
            centroids = data[indices].copy()
            
            for _ in range(max_iter):
                distances = cp.dot(data, centroids.T)
                labels = cp.argmax(distances, axis=1)
                
                new_centroids = cp.zeros_like(centroids)
                for i in range(k):
                    mask = labels == i
                    if cp.sum(mask) > 0:
                        new_centroids[i] = cp.mean(data[mask], axis=0)
                
                if cp.linalg.norm(new_centroids - centroids) < tol:
                    break
                centroids = new_centroids
            
            return (
                self.to_cpu(labels),
                self.to_cpu(centroids)
            )
        
        from sklearn.cluster import KMeans
        kmeans = KMeans(n_clusters=k, max_iter=max_iter)
        labels = kmeans.fit_predict(data)
        return labels, kmeans.cluster_centers_


class GPUConvolution:
    def __init__(self, accelerator: GPUAccelerator):
        self.accelerator = accelerator
    
    def apply_filter(
        self,
        signal: np.ndarray,
        kernel: np.ndarray
    ) -> np.ndarray:
        if self.accelerator.gpu_available:
            s = self.accelerator.to_gpu(signal)
            k = self.accelerator.to_gpu(kernel)
            
            result = cp.convolve(s, k, mode='same')
            return self.accelerator.to_cpu(result)
        
        return np.convolve(signal, kernel, mode='same')
    
    def sliding_window_dot(
        self,
        matrix: np.ndarray,
        window_size: int
    ) -> np.ndarray:
        if self.accelerator.gpu_available:
            m = self.accelerator.to_gpu(matrix)
            
            from cupyx.scipy import ndimage
            result = ndimage.uniform_filter1d(m, window_size, mode='constant')
            return self.accelerator.to_cpu(result)
        
        from scipy.ndimage import uniform_filter1d
        return uniform_filter1d(matrix, window_size, mode='constant')


class GPUMemoryPool:
    def __init__(self):
        self.pool = {}
    
    def allocate(self, shape: Tuple[int, ...], dtype=np.float32) -> "cp.ndarray":
        if GPU_AVAILABLE:
            key = (shape, dtype)
            if key in self.pool:
                return self.pool.pop(key)
            return cp.zeros(shape, dtype=dtype)
        return np.zeros(shape, dtype=dtype)
    
    def release(self, array):
        if GPU_AVAILABLE and isinstance(array, cp.ndarray):
            key = (array.shape, array.dtype)
            self.pool[key] = array


accelerator = GPUAccelerator()
memory_pool = GPUMemoryPool()


def gpu_enabled() -> bool:
    return GPU_AVAILABLE


def get_device_info() -> dict:
    if GPU_AVAILABLE:
        device = cp.cuda.Device()
        props = cp.cuda.runtime.getDeviceProperties(device.id)
        return {
            "available": True,
            "name": props["name"].decode(),
            "total_memory": props["totalGlobalMem"] / (1024**3),
            "compute_capability": f"{props['major']}.{props['minor']}"
        }
    return {"available": False}


if __name__ == "__main__":
    print(f"GPU Available: {gpu_enabled()}")
    print(f"Device Info: {get_device_info()}")
    
    if GPU_AVAILABLE:
        data = np.random.randn(1000, 512)
        acc = GPUAccelerator()
        labels, centroids = acc.kmeans_gpu(data, k=5)
        print(f"K-means complete. Labels shape: {labels.shape}")
