import numpy as np

class LSTMGeneralization:
    def __init__(self, input_size=3, hidden_size=2):
        # Shared weights for all sequences and positions
        self.W = np.random.randn(input_size, hidden_size) * 0.1
        self.b = np.zeros(hidden_size)
    
    def process_sequence(self, sequence):
        """Can handle any sequence length due to weight sharing"""
        states = []
        h = np.zeros(self.W.shape[1])  # Initial state
        
        for element in sequence:
            h = np.tanh(np.dot(element, self.W) + self.b)
            states.append(h)
        return states

# Example 1: Length Generalization
def demonstrate_length_generalization():
    print("=== Length Generalization Example ===")
    lstm = LSTMGeneralization()
    
    # Training on short sequences
    short_sequence = np.array([
        [1, 0, 0],
        [0, 1, 0]
    ])
    
    # Can generalize to longer sequences
    long_sequence = np.array([
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1],
        [1, 1, 0],
        [0, 1, 1]
    ])
    
    print("\nProcessing short sequence (length 2):")
    short_results = lstm.process_sequence(short_sequence)
    for i, state in enumerate(short_results):
        print(f"Step {i+1} output:", state)
        
    print("\nProcessing long sequence (length 5) with same weights:")
    long_results = lstm.process_sequence(long_sequence)
    for i, state in enumerate(long_results):
        print(f"Step {i+1} output:", state)

# Example 2: Pattern Position Invariance
def demonstrate_pattern_invariance():
    print("\n=== Pattern Position Invariance Example ===")
    lstm = LSTMGeneralization()
    
    # Same pattern in different positions
    pattern1 = np.array([
        [1, 0, 0],  # Pattern start
        [0, 1, 0],
        [0, 0, 1]
    ])
    
    pattern2 = np.array([
        [0, 0, 0],
        [1, 0, 0],  # Same pattern, different position
        [0, 1, 0],
        [0, 0, 1]
    ])
    
    print("\nPattern in first position:")
    results1 = lstm.process_sequence(pattern1)
    
    print("\nSame pattern in later position:")
    results2 = lstm.process_sequence(pattern2)
    
    # Compare pattern recognition
    def find_pattern_activation(states):
        return [np.mean(np.abs(state)) for state in states]
    
    act1 = find_pattern_activation(results1)
    act2 = find_pattern_activation(results2)
    
    print("\nPattern activation levels:")
    print("First position:", act1)
    print("Shifted position:", act2)

# Example 3: Scale Invariance
def demonstrate_scale_invariance():
    print("\n=== Scale Invariance Example ===")
    lstm = LSTMGeneralization()
    
    # Same pattern at different scales
    original_pattern = np.array([
        [0.1, 0.2, 0.3],
        [0.2, 0.4, 0.6],
        [0.1, 0.2, 0.3]
    ])
    
    scaled_pattern = original_pattern * 2
    
    print("\nOriginal pattern responses:")
    original_results = lstm.process_sequence(original_pattern)
    for i, state in enumerate(original_results):
        print(f"Step {i+1}:", state)
    
    print("\nScaled pattern responses:")
    scaled_results = lstm.process_sequence(scaled_pattern)
    for i, state in enumerate(scaled_results):
        print(f"Step {i+1}:", state)

# Run demonstrations
demonstrate_length_generalization()
demonstrate_pattern_invariance()
demonstrate_scale_invariance()