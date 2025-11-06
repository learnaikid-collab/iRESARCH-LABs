# Advanced Optimization Algorithms

This document provides detailed explanations of the core optimization algorithms used in the Prompt Optimization System.

## Table of Contents

1. [Mesa-Optimization](#1-mesa-optimization)
2. [Reinforcement Learning (RLPrompt)](#2-reinforcement-learning-rlprompt)
3. [Evolutionary Optimization (PromptBreeder)](#3-evolutionary-optimization-promptbreeder)
4. [Self-Critique Refinement (PromptWizard)](#4-self-critique-refinement-promptwizard)
5. [Multi-Objective Optimization (SAMMO)](#5-multi-objective-optimization-sammo)
6. [Chain-of-Thought Strategies](#6-chain-of-thought-strategies)
7. [Retrieval-Augmented Generation](#7-retrieval-augmented-generation)

---

## 1. Mesa-Optimization

### Concept

Mesa-optimization refers to an internal optimizer that operates within the system to continuously improve prompts. The term comes from AI safety research where "mesa-optimizers" are learned sub-processes that pursue their own objectives.

### Our Implementation

We repurpose this constructively by creating an inner-loop optimizer explicitly aligned with user goals.

### Algorithm

```python
def mesa_optimize(
    prompt: Prompt,
    user_goal: Goal,
    llm_engine: LLMEngine,
    max_iterations: int = 10
) -> Prompt:
    """
    Mesa-optimization loop for prompt refinement.
    
    Args:
        prompt: Initial prompt
        user_goal: User's objective (embedded in reward function)
        llm_engine: LLM for generation
        max_iterations: Maximum optimization steps
        
    Returns:
        Optimized prompt
    """
    # Initialize inner optimizer
    inner_optimizer = InnerLoopOptimizer(
        goal=user_goal,
        search_strategy='beam_search',  # or 'evolutionary', 'gradient_free'
        beam_width=5
    )
    
    current_prompt = prompt
    best_prompt = prompt
    best_score = float('-inf')
    
    for iteration in range(max_iterations):
        # Inner optimizer generates candidate modifications
        candidates = inner_optimizer.generate_candidates(
            current_prompt,
            n_candidates=inner_optimizer.beam_width
        )
        
        # Evaluate each candidate
        scores = []
        outputs = []
        for candidate in candidates:
            output = llm_engine.generate(candidate)
            score = compute_reward(output, user_goal)
            scores.append(score)
            outputs.append(output)
        
        # Update best
        max_idx = np.argmax(scores)
        if scores[max_idx] > best_score:
            best_score = scores[max_idx]
            best_prompt = candidates[max_idx]
        
        # Inner optimizer updates its strategy
        inner_optimizer.update(
            candidates=candidates,
            scores=scores,
            outputs=outputs
        )
        
        # Check convergence
        if inner_optimizer.has_converged():
            break
        
        # Move to best candidate for next iteration
        current_prompt = best_prompt
    
    return best_prompt


class InnerLoopOptimizer:
    """Inner optimizer with its own search strategy."""
    
    def __init__(self, goal: Goal, search_strategy: str, beam_width: int):
        self.goal = goal
        self.strategy = search_strategy
        self.beam_width = beam_width
        self.history = []
        
    def generate_candidates(
        self,
        prompt: Prompt,
        n_candidates: int
    ) -> List[Prompt]:
        """Generate prompt variations to explore."""
        
        if self.strategy == 'beam_search':
            return self._beam_search_candidates(prompt, n_candidates)
        elif self.strategy == 'evolutionary':
            return self._evolutionary_candidates(prompt, n_candidates)
        elif self.strategy == 'gradient_free':
            return self._gradient_free_candidates(prompt, n_candidates)
    
    def _beam_search_candidates(
        self,
        prompt: Prompt,
        n: int
    ) -> List[Prompt]:
        """Generate candidates through structured modifications."""
        candidates = []
        
        # Strategy 1: Paraphrase instruction
        candidates.append(prompt.paraphrase_instruction())
        
        # Strategy 2: Add/remove examples
        if prompt.has_examples():
            candidates.append(prompt.remove_example())
        else:
            candidates.append(prompt.add_example())
        
        # Strategy 3: Adjust verbosity
        candidates.append(prompt.make_more_detailed())
        candidates.append(prompt.make_more_concise())
        
        # Strategy 4: Change format
        candidates.append(prompt.change_format('bullet_points'))
        candidates.append(prompt.change_format('numbered_steps'))
        
        return candidates[:n]
    
    def update(
        self,
        candidates: List[Prompt],
        scores: List[float],
        outputs: List[str]
    ):
        """Learn from evaluation results."""
        # Record what worked
        self.history.append({
            'candidates': candidates,
            'scores': scores,
            'outputs': outputs
        })
        
        # Adjust strategy based on performance
        # (e.g., if adding examples helped, prefer that)
        self._adapt_strategy()
    
    def has_converged(self) -> bool:
        """Check if optimization has plateaued."""
        if len(self.history) < 3:
            return False
        
        recent_scores = [max(h['scores']) for h in self.history[-3:]]
        variance = np.var(recent_scores)
        return variance < 0.01  # Threshold for convergence
```

### Key Features

1. **Alignment**: Inner optimizer's reward is derived from user goal
2. **Search Strategies**: Multiple exploration methods
3. **Adaptive**: Learns which modifications work
4. **Convergence Detection**: Stops when improvements plateau

---

## 2. Reinforcement Learning (RLPrompt)

### Concept

Treat prompt optimization as an RL problem where:
- **State**: Current prompt
- **Action**: Modification to apply
- **Reward**: Quality score of resulting output

### Algorithm

```python
class RLPromptOptimizer:
    """RL-based prompt optimization using policy gradients."""
    
    def __init__(self, llm_engine: LLMEngine, policy_config: Dict):
        self.llm = llm_engine
        self.policy = PromptPolicy(config=policy_config)
        self.optimizer = torch.optim.Adam(self.policy.parameters(), lr=1e-4)
        
    def optimize(
        self,
        initial_prompt: Prompt,
        query: str,
        n_episodes: int = 100
    ) -> Prompt:
        """Optimize prompt using RL."""
        
        for episode in range(n_episodes):
            # Sample action from policy
            state = self.encode_prompt(initial_prompt)
            action, log_prob = self.policy.sample_action(state)
            
            # Apply action to get new prompt
            new_prompt = self.apply_action(initial_prompt, action)
            
            # Generate output and compute reward
            output = self.llm.generate(new_prompt)
            reward = self.compute_reward(output, query)
            
            # Policy gradient update
            loss = -log_prob * reward  # REINFORCE algorithm
            
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()
            
            # Update prompt if improved
            if reward > best_reward:
                best_prompt = new_prompt
                best_reward = reward
        
        return best_prompt
    
    def apply_action(self, prompt: Prompt, action: Action) -> Prompt:
        """Apply modification action to prompt."""
        action_type, params = action
        
        if action_type == 'add_instruction':
            return prompt.add_instruction(params['text'])
        elif action_type == 'rephrase_section':
            return prompt.rephrase_section(params['section_id'], params['new_text'])
        elif action_type == 'add_example':
            return prompt.add_example(params['example'])
        elif action_type == 'remove_section':
            return prompt.remove_section(params['section_id'])
        # ... more action types
        
    def compute_reward(self, output: str, query: str) -> float:
        """Compute reward from output quality."""
        # Could use:
        # - Learned reward model
        # - Heuristic metrics
        # - LLM-as-judge
        
        reward = 0.0
        
        # Completeness: Does it answer the query?
        reward += self.check_completeness(output, query) * 0.3
        
        # Correctness: Is it factually accurate?
        reward += self.check_correctness(output) * 0.3
        
        # Coherence: Is it well-structured?
        reward += self.check_coherence(output) * 0.2
        
        # Length appropriateness
        reward += self.check_length(output, query) * 0.2
        
        return reward


class PromptPolicy(nn.Module):
    """Neural network policy for prompt actions."""
    
    def __init__(self, config: Dict):
        super().__init__()
        self.encoder = nn.TransformerEncoder(...)
        self.action_head = nn.Linear(hidden_dim, n_actions)
        
    def sample_action(self, state: Tensor) -> Tuple[Action, Tensor]:
        """Sample action and return log probability."""
        encoded = self.encoder(state)
        logits = self.action_head(encoded)
        
        # Sample from categorical distribution
        dist = Categorical(logits=logits)
        action_idx = dist.sample()
        log_prob = dist.log_prob(action_idx)
        
        action = self.decode_action(action_idx)
        return action, log_prob
```

### Key Features

1. **Policy Network**: Learns prompt modification strategy
2. **REINFORCE Algorithm**: Classic policy gradient method
3. **Reward Shaping**: Multiple components for comprehensive evaluation
4. **Discrete Actions**: Handles non-differentiable prompt space

### Optimization Techniques

- **Baseline Subtraction**: Reduce variance
- **Reward Normalization**: Stabilize learning
- **Entropy Regularization**: Encourage exploration

---

## 3. Evolutionary Optimization (PromptBreeder)

### Concept

Evolve a population of prompts through selection, mutation, and crossover, guided by the LLM itself.

### Algorithm

```python
class PromptBreeder:
    """Self-referential evolutionary prompt optimization."""
    
    def __init__(
        self,
        llm_engine: LLMEngine,
        population_size: int = 20,
        n_generations: int = 10
    ):
        self.llm = llm_engine
        self.population_size = population_size
        self.n_generations = n_generations
        
    def optimize(
        self,
        initial_prompt: Prompt,
        query: str
    ) -> Prompt:
        """Evolve prompts through generations."""
        
        # Initialize population
        population = self.initialize_population(initial_prompt)
        mutation_strategies = self.initialize_mutation_strategies()
        
        for generation in range(self.n_generations):
            # Evaluate fitness
            fitness_scores = []
            for prompt in population:
                output = self.llm.generate(prompt)
                fitness = self.evaluate_fitness(output, query)
                fitness_scores.append(fitness)
            
            # Selection
            parents = self.select_parents(population, fitness_scores)
            
            # Generate offspring through mutation
            offspring = []
            for parent in parents:
                # Select mutation strategy
                strategy = random.choice(mutation_strategies)
                
                # LLM-guided mutation
                mutated = self.mutate_prompt(parent, strategy)
                offspring.append(mutated)
            
            # Optional: Crossover
            if len(offspring) >= 2:
                crossed = self.crossover(offspring[0], offspring[1])
                offspring.append(crossed)
            
            # Evolve mutation strategies themselves (self-referential!)
            mutation_strategies = self.evolve_strategies(
                mutation_strategies,
                population,
                fitness_scores
            )
            
            # New population = best parents + offspring
            combined = parents + offspring
            combined_fitness = fitness_scores[:len(parents)] + \
                              [self.evaluate_fitness(
                                  self.llm.generate(p), query
                              ) for p in offspring]
            
            # Keep top performers
            sorted_indices = np.argsort(combined_fitness)[::-1]
            population = [combined[i] for i in sorted_indices[:self.population_size]]
        
        # Return best prompt
        final_fitness = [self.evaluate_fitness(
            self.llm.generate(p), query
        ) for p in population]
        best_idx = np.argmax(final_fitness)
        return population[best_idx]
    
    def mutate_prompt(
        self,
        prompt: Prompt,
        strategy: MutationStrategy
    ) -> Prompt:
        """Use LLM to mutate prompt according to strategy."""
        
        mutation_prompt = f"""
        Given this prompt:
        {prompt}
        
        Apply this mutation strategy:
        {strategy.description}
        
        Generate an improved variant of the prompt.
        """
        
        mutated_text = self.llm.generate(mutation_prompt)
        return Prompt.from_text(mutated_text)
    
    def evolve_strategies(
        self,
        strategies: List[MutationStrategy],
        population: List[Prompt],
        fitness: List[float]
    ) -> List[MutationStrategy]:
        """Evolve the mutation strategies themselves (meta-evolution)."""
        
        # Evaluate which strategies led to good prompts
        strategy_effectiveness = defaultdict(list)
        for i, prompt in enumerate(population):
            if hasattr(prompt, 'strategy_used'):
                strategy_effectiveness[prompt.strategy_used].append(fitness[i])
        
        # Generate new strategies
        best_strategy = max(
            strategies,
            key=lambda s: np.mean(strategy_effectiveness.get(s.id, [0]))
        )
        
        new_strategy_prompt = f"""
        This mutation strategy worked well:
        {best_strategy.description}
        
        Create a new, potentially better mutation strategy for prompts.
        Be creative but maintain coherence.
        """
        
        new_strategy_desc = self.llm.generate(new_strategy_prompt)
        new_strategy = MutationStrategy(
            id=f"gen_{len(strategies)}",
            description=new_strategy_desc
        )
        
        # Keep best strategies + new ones
        strategies.append(new_strategy)
        return strategies[-10:]  # Keep last 10 strategies
    
    def crossover(self, prompt1: Prompt, prompt2: Prompt) -> Prompt:
        """Combine two prompts."""
        
        crossover_prompt = f"""
        Combine these two prompts into a single, cohesive prompt
        that captures the strengths of both:
        
        Prompt 1:
        {prompt1}
        
        Prompt 2:
        {prompt2}
        
        Create a hybrid prompt:
        """
        
        hybrid_text = self.llm.generate(crossover_prompt)
        return Prompt.from_text(hybrid_text)
```

### Key Features

1. **Self-Referential**: LLM evolves both prompts and mutation strategies
2. **Population Diversity**: Maintains multiple prompt variants
3. **Meta-Evolution**: Strategies themselves evolve
4. **Genetic Operators**: Selection, mutation, crossover

### Mutation Strategies Examples

```python
mutation_strategies = [
    MutationStrategy(
        id="simplify",
        description="Make the prompt simpler and more direct"
    ),
    MutationStrategy(
        id="add_examples",
        description="Add relevant examples to guide the model"
    ),
    MutationStrategy(
        id="restructure",
        description="Reorganize the prompt for better clarity"
    ),
    MutationStrategy(
        id="add_constraints",
        description="Add specific constraints or requirements"
    )
]
```

---

## 4. Self-Critique Refinement (PromptWizard)

### Concept

Use the LLM itself to critique and improve its outputs through iterative reflection.

### Algorithm

```python
class SelfCritiqueOptimizer:
    """PromptWizard-style self-improvement through critique."""
    
    def __init__(self, llm_engine: LLMEngine):
        self.llm = llm_engine
        
    def optimize(
        self,
        initial_prompt: Prompt,
        query: str,
        max_iterations: int = 5
    ) -> Prompt:
        """Iteratively improve through self-critique."""
        
        current_prompt = initial_prompt
        
        for iteration in range(max_iterations):
            # Generate output
            output = self.llm.generate(current_prompt)
            
            # Self-critique
            critique = self.generate_critique(query, output, current_prompt)
            
            # Check if satisfactory
            if critique.is_satisfactory:
                break
            
            # Improve prompt based on critique
            improved_prompt = self.improve_prompt(
                current_prompt,
                critique
            )
            
            # Validate improvement
            if self.is_actually_better(improved_prompt, current_prompt, query):
                current_prompt = improved_prompt
            else:
                # If not better, try different improvement strategy
                current_prompt = self.alternative_improvement(
                    current_prompt,
                    critique
                )
        
        return current_prompt
    
    def generate_critique(
        self,
        query: str,
        output: str,
        prompt: Prompt
    ) -> Critique:
        """Ask LLM to critique its own output."""
        
        critique_prompt = f"""
        Original Query: {query}
        
        Prompt Used: {prompt}
        
        Output Generated: {output}
        
        Analyze this output comprehensively:
        1. Does it fully answer the query?
        2. Is it accurate and factual?
        3. Is the structure and format appropriate?
        4. What's missing or could be improved?
        5. How should the prompt be modified to get a better answer?
        
        Be specific and actionable in your critique.
        """
        
        critique_text = self.llm.generate(critique_prompt)
        return Critique.parse(critique_text)
    
    def improve_prompt(
        self,
        prompt: Prompt,
        critique: Critique
    ) -> Prompt:
        """Apply critique to improve prompt."""
        
        improvement_prompt = f"""
        Current Prompt:
        {prompt}
        
        Critique and Improvement Suggestions:
        {critique.suggestions}
        
        Generate an improved version of the prompt that addresses
        the issues raised in the critique. Maintain the core intent
        but modify structure, instructions, or examples as needed.
        
        Improved Prompt:
        """
        
        improved_text = self.llm.generate(improvement_prompt)
        return Prompt.from_text(improved_text)
    
    def is_actually_better(
        self,
        new_prompt: Prompt,
        old_prompt: Prompt,
        query: str
    ) -> bool:
        """Verify that new prompt actually produces better output."""
        
        old_output = self.llm.generate(old_prompt)
        new_output = self.llm.generate(new_prompt)
        
        old_score = self.evaluate_output(old_output, query)
        new_score = self.evaluate_output(new_output, query)
        
        return new_score > old_score


@dataclass
class Critique:
    is_satisfactory: bool
    issues: List[str]
    suggestions: List[str]
    priority_fixes: List[str]
    
    @classmethod
    def parse(cls, text: str) -> 'Critique':
        """Parse critique from LLM response."""
        # Extract structured information from critique text
        # (implementation depends on expected format)
        pass
```

### Key Features

1. **Self-Awareness**: LLM critiques its own output
2. **Iterative**: Multiple rounds of improvement
3. **Validation**: Ensures changes actually help
4. **Actionable**: Critiques include specific improvements

### Advanced: Joint Optimization

```python
class JointOptimizer(SelfCritiqueOptimizer):
    """Optimize both instructions and examples together."""
    
    def improve_prompt(
        self,
        prompt: Prompt,
        critique: Critique
    ) -> Prompt:
        """Improve both instruction and examples."""
        
        # Improve instruction
        new_instruction = self.improve_instruction(
            prompt.instruction,
            critique
        )
        
        # Improve or generate examples
        new_examples = self.improve_examples(
            prompt.examples,
            critique,
            prompt.instruction
        )
        
        return Prompt(
            instruction=new_instruction,
            examples=new_examples,
            format=prompt.format
        )
    
    def improve_examples(
        self,
        current_examples: List[Example],
        critique: Critique,
        instruction: str
    ) -> List[Example]:
        """Generate better examples based on critique."""
        
        example_improvement_prompt = f"""
        Instruction: {instruction}
        
        Current Examples: {current_examples}
        
        Critique: {critique.suggestions}
        
        Generate improved examples that:
        1. Better illustrate the task
        2. Address the issues in the critique
        3. Are diverse and representative
        
        Provide 2-3 high-quality examples:
        """
        
        examples_text = self.llm.generate(example_improvement_prompt)
        return self.parse_examples(examples_text)
```

---

## 5. Multi-Objective Optimization (SAMMO)

### Concept

Optimize prompts across multiple objectives simultaneously (accuracy, brevity, safety, etc.).

### Algorithm

```python
class MultiObjectiveOptimizer:
    """SAMMO-inspired multi-objective prompt optimization."""
    
    def __init__(self, llm_engine: LLMEngine):
        self.llm = llm_engine
        
    def optimize(
        self,
        initial_prompt: Prompt,
        query: str,
        objectives: List[Objective],
        strategy: str = 'pareto'
    ) -> Prompt:
        """Optimize across multiple objectives."""
        
        if strategy == 'pareto':
            return self.pareto_optimization(initial_prompt, query, objectives)
        elif strategy == 'weighted':
            return self.weighted_optimization(initial_prompt, query, objectives)
        elif strategy == 'lexicographic':
            return self.lexicographic_optimization(initial_prompt, query, objectives)
    
    def pareto_optimization(
        self,
        initial_prompt: Prompt,
        query: str,
        objectives: List[Objective]
    ) -> Prompt:
        """Find Pareto-optimal prompt."""
        
        # Generate population of prompts
        population = self.generate_diverse_prompts(initial_prompt, n=50)
        
        # Evaluate each on all objectives
        scores_matrix = []
        for prompt in population:
            output = self.llm.generate(prompt)
            scores = [obj.evaluate(output, query) for obj in objectives]
            scores_matrix.append(scores)
        
        # Find Pareto frontier
        pareto_indices = self.compute_pareto_frontier(scores_matrix)
        pareto_prompts = [population[i] for i in pareto_indices]
        
        # Select from Pareto set (e.g., use knee point)
        best_idx = self.select_from_pareto(
            [scores_matrix[i] for i in pareto_indices],
            objectives
        )
        
        return pareto_prompts[best_idx]
    
    def weighted_optimization(
        self,
        initial_prompt: Prompt,
        query: str,
        objectives: List[Objective]
    ) -> Prompt:
        """Weighted sum of objectives."""
        
        def combined_score(prompt: Prompt) -> float:
            output = self.llm.generate(prompt)
            score = 0.0
            for obj in objectives:
                score += obj.weight * obj.evaluate(output, query)
            return score
        
        # Use any single-objective optimizer with combined score
        return self.optimize_single_objective(
            initial_prompt,
            query,
            score_fn=combined_score
        )
    
    def structured_edit(
        self,
        prompt: Prompt,
        operation: StructuredOperation
    ) -> Prompt:
        """Apply structured modification to prompt."""
        
        if operation.type == 'remove_section':
            return prompt.remove_section(operation.section_id)
        elif operation.type == 'compress_section':
            return prompt.compress_section(
                operation.section_id,
                target_length=operation.target_length
            )
        elif operation.type == 'reorder':
            return prompt.reorder_sections(operation.new_order)
        # ... more operations


class Objective:
    """Single optimization objective."""
    
    def __init__(self, name: str, evaluator: Callable, weight: float = 1.0):
        self.name = name
        self.evaluator = evaluator
        self.weight = weight
        
    def evaluate(self, output: str, query: str) -> float:
        """Evaluate objective on output."""
        return self.evaluator(output, query)


# Example objectives
objectives = [
    Objective(
        name="accuracy",
        evaluator=lambda out, q: measure_accuracy(out, q),
        weight=0.5
    ),
    Objective(
        name="brevity",
        evaluator=lambda out, q: 1.0 / (1.0 + len(out.split())),
        weight=0.2
    ),
    Objective(
        name="clarity",
        evaluator=lambda out, q: measure_readability(out),
        weight=0.3
    )
]
```

### Key Features

1. **Multiple Objectives**: Balance competing goals
2. **Pareto Optimization**: Find non-dominated solutions
3. **Structured Edits**: Surgical prompt modifications
4. **Flexible Strategies**: Pareto, weighted, lexicographic

---

## 6. Chain-of-Thought Strategies

### Standard CoT

```python
def apply_cot(prompt: Prompt) -> Prompt:
    """Add chain-of-thought trigger."""
    return prompt.add_instruction(
        "Let's think step by step and reason through this carefully."
    )
```

### Zero-Shot CoT

```python
def zero_shot_cot(query: str) -> Prompt:
    """Zero-shot chain-of-thought."""
    return Prompt(f"{query}\n\nLet's approach this step-by-step:")
```

### Few-Shot CoT

```python
def few_shot_cot(query: str, domain: str) -> Prompt:
    """Few-shot with reasoning examples."""
    examples = get_cot_examples(domain)
    
    prompt = Prompt()
    for ex in examples:
        prompt.add_example(ex.question, ex.reasoning, ex.answer)
    prompt.add_query(query)
    
    return prompt
```

### Self-Consistency

```python
def self_consistency_cot(
    prompt: Prompt,
    llm: LLMEngine,
    n_samples: int = 5
) -> str:
    """Sample multiple reasoning paths and vote."""
    
    outputs = []
    for _ in range(n_samples):
        output = llm.generate(prompt, temperature=0.7)
        outputs.append(output)
    
    # Extract final answers
    answers = [extract_final_answer(out) for out in outputs]
    
    # Majority vote
    return most_common(answers)
```

---

## 7. Retrieval-Augmented Generation

### RAG Pipeline

```python
class RAGSystem:
    """Retrieval-augmented generation."""
    
    def __init__(self):
        self.retriever = DenseRetriever()
        self.reranker = CrossEncoderReranker()
        
    def augment_prompt(
        self,
        query: str,
        prompt: Prompt,
        k: int = 5
    ) -> Prompt:
        """Add retrieved context to prompt."""
        
        # Retrieve relevant documents
        candidates = self.retriever.retrieve(query, k=20)
        
        # Rerank for relevance
        reranked = self.reranker.rerank(query, candidates, k=k)
        
        # Format context
        context = self.format_context(reranked)
        
        # Insert into prompt
        return prompt.add_context(context, position='after_instruction')
    
    def format_context(self, documents: List[Document]) -> str:
        """Format retrieved docs for prompt."""
        context_parts = []
        for i, doc in enumerate(documents, 1):
            context_parts.append(
                f"[Source {i}]: {doc.title}\n{doc.content}\n"
            )
        return "\n".join(context_parts)
```

### Web Search Integration

```python
class WebSearchRAG(RAGSystem):
    """RAG with live web search."""
    
    def __init__(self, search_api: SearchAPI):
        super().__init__()
        self.search = search_api
        
    def augment_prompt(
        self,
        query: str,
        prompt: Prompt,
        k: int = 5
    ) -> Prompt:
        """Augment with web search results."""
        
        # Perform web search
        search_results = self.search.search(query, num_results=10)
        
        # Extract and process content
        documents = [
            self.extract_content(result.url)
            for result in search_results
        ]
        
        # Standard RAG pipeline
        return super().augment_prompt(
            query,
            prompt,
            k=k,
            documents=documents
        )
```

---

## Algorithm Selection Strategy

```python
class AlgorithmSelector:
    """Automatically select best optimization algorithm."""
    
    def select(self, task_analysis: TaskAnalysis) -> str:
        """Select optimization strategy based on task."""
        
        if task_analysis.complexity == 'simple':
            return 'self_critique'  # Fast, good for simple tasks
            
        elif task_analysis.requires_reasoning:
            return 'mesa_optimization'  # Good for complex reasoning
            
        elif task_analysis.has_multiple_objectives:
            return 'multi_objective'  # Handle trade-offs
            
        elif task_analysis.needs_creative_exploration:
            return 'evolutionary'  # Explore diverse solutions
            
        else:
            return 'rl'  # General purpose
```

---

## Performance Comparison

| Algorithm | Speed | Quality | Exploration | Use Case |
|-----------|-------|---------|-------------|----------|
| Mesa-Optimization | Medium | High | Medium | Complex reasoning |
| RL (RLPrompt) | Slow | High | High | General purpose |
| Evolutionary | Medium | Very High | Very High | Creative tasks |
| Self-Critique | Fast | Medium | Low | Simple improvements |
| Multi-Objective | Slow | High | Medium | Trade-off optimization |

---

**Document Version**: 1.0  
**Last Updated**: 2025-11-06
