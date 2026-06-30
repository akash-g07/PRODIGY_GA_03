"""
Simple text generation using a word-level Markov chain.
"""

import random
import re
from collections import defaultdict

class MarkovChain:
    def __init__(self, order=2):
        self.order = order
        self.model = defaultdict(list)

    def train(self, text):
        words = re.findall(r"\b\w+\b|[.,!?;]", text)
        for i in range(len(words) - self.order):
            key = tuple(words[i:i + self.order])
            next_word = words[i + self.order]
            self.model[key].append(next_word)

    def generate(self, length=50, seed=None):
        if not self.model:
            raise ValueError("Model has not been trained yet.")

        if seed and tuple(seed) in self.model:
            current = tuple(seed)
        else:
            current = random.choice(list(self.model.keys()))

        result = list(current)

        for _ in range(length - self.order):
            possible_next = self.model.get(current)
            if not possible_next:
                current = random.choice(list(self.model.keys()))
                possible_next = self.model[current]
            next_word = random.choice(possible_next)
            result.append(next_word)
            current = tuple(result[-self.order:])

        text = " ".join(result)
        text = re.sub(r"\s+([.,!?;])", r"\1", text)
        return text


if __name__ == "__main__":
    sample_text = """
    Machine learning is a method of data analysis that automates analytical
    model building. It is a branch of artificial intelligence based on the
    idea that systems can learn from data, identify patterns and make
    decisions with minimal human intervention. Machine learning algorithms
    build a model based on sample data, known as training data, in order to
    make predictions or decisions without being explicitly programmed to do so.
    """

    mc = MarkovChain(order=2)
    mc.train(sample_text)
    generated = mc.generate(length=40)
    print("Generated text:")
    print(generated)
