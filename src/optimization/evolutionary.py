"""
Evolutionary Optimizer - PromptBreeder implementation.

Uses evolutionary algorithms to breed and mutate prompts for optimization.
"""

import logging
import random
from typing import List, Tuple, Optional
from dataclasses import dataclass

from src.core.llm_engine import LLMEngine
from src.core.task_analyzer import TaskAnalysis

logger = logging.getLogger(__name__)


@dataclass
class Individual:
    """An individual in the population (a prompt)."""
    prompt: str
    fitness: float = 0.0
    generation: int = 0


class EvolutionaryOptimizer:
    """
    Evolutionary prompt optimization using genetic algorithms.
    
    Implements PromptBreeder methodology with:
    - Population-based search
    - Mutation and crossover operators
    - Fitness evaluation
    - Elitism and diversity maintenance
    """
    
    def __init__(
        self,
        engine: LLMEngine,
        population_size: int = 20,
        mutation_rate: float = 0.2,
        crossover_rate: float = 0.7,
        generations: int = 50,
        elitism_ratio: float = 0.1,
    ):
        """Initialize the Evolutionary Optimizer."""
        self.engine = engine
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.generations = generations
        self.elitism_ratio = elitism_ratio
        
        logger.info(
            f"Evolutionary Optimizer initialized: pop={population_size}, "
            f"gens={generations}"
        )
    
    def optimize(
        self,
        initial_prompt: str,
        task_analysis: TaskAnalysis,
    ) -> str:
        """
        Optimize prompt using evolutionary algorithm.
        
        Args:
            initial_prompt: Starting prompt
            task_analysis: Task analysis
            
        Returns:
            Optimized prompt
        """
        logger.info("Starting evolutionary optimization")
        
        # Initialize population
        population = self._initialize_population(initial_prompt, task_analysis)
        
        # Evolve for specified generations
        for generation in range(self.generations):
            # Evaluate fitness
            population = self._evaluate_population(population, task_analysis)
            
            # Sort by fitness
            population.sort(key=lambda x: x.fitness, reverse=True)
            
            logger.debug(
                f"Generation {generation + 1}: "
                f"Best fitness={population[0].fitness:.3f}"
            )
            
            # Early stopping if converged
            if population[0].fitness >= 0.95:
                break
            
            # Create next generation
            population = self._create_next_generation(population, task_analysis)
        
        # Return best individual
        best = max(population, key=lambda x: x.fitness)
        logger.info(f"Evolution complete: best fitness={best.fitness:.3f}")
        
        return best.prompt
    
    def _initialize_population(
        self,
        initial_prompt: str,
        task_analysis: TaskAnalysis
    ) -> List[Individual]:
        """Initialize population with variations of initial prompt."""
        population = [Individual(initial_prompt, generation=0)]
        
        # Generate variations
        for i in range(self.population_size - 1):
            variation = self._mutate(initial_prompt, task_analysis)
            population.append(Individual(variation, generation=0))
        
        return population
    
    def _mutate(self, prompt: str, task_analysis: TaskAnalysis) -> str:
        """Apply mutation to a prompt."""
        mutation_prompt = f"""Create a variation of this prompt while maintaining its core intent:

Original: {prompt}

Task: {task_analysis.task_type.value}

Provide ONLY the mutated prompt:"""
        
        try:
            result = self.engine.generate(mutation_prompt, temperature=0.9)
            return result.text.strip()
        except:
            return prompt
    
    def _crossover(
        self,
        parent1: str,
        parent2: str,
        task_analysis: TaskAnalysis
    ) -> str:
        """Combine two prompts via crossover."""
        crossover_prompt = f"""Combine the best elements of these two prompts:

Prompt 1: {parent1}

Prompt 2: {parent2}

Create a new prompt that inherits strengths from both.
Provide ONLY the new prompt:"""
        
        try:
            result = self.engine.generate(crossover_prompt, temperature=0.7)
            return result.text.strip()
        except:
            return parent1
    
    def _evaluate_population(
        self,
        population: List[Individual],
        task_analysis: TaskAnalysis
    ) -> List[Individual]:
        """Evaluate fitness of all individuals."""
        for individual in population:
            if individual.fitness == 0.0:  # Not yet evaluated
                individual.fitness = self._evaluate_fitness(
                    individual.prompt,
                    task_analysis
                )
        return population
    
    def _evaluate_fitness(self, prompt: str, task_analysis: TaskAnalysis) -> float:
        """Evaluate fitness of a single prompt."""
        eval_prompt = f"""Rate this prompt's quality (0.0-1.0): {prompt}"""
        
        try:
            result = self.engine.generate(eval_prompt, temperature=0.3, max_tokens=10)
            return max(0.0, min(1.0, float(result.text.strip())))
        except:
            return 0.5
    
    def _create_next_generation(
        self,
        population: List[Individual],
        task_analysis: TaskAnalysis
    ) -> List[Individual]:
        """Create next generation using selection, crossover, and mutation."""
        next_gen = []
        
        # Elitism: keep top performers
        elite_count = int(self.population_size * self.elitism_ratio)
        next_gen.extend(population[:elite_count])
        
        # Fill rest with offspring
        while len(next_gen) < self.population_size:
            # Selection
            parent1 = self._tournament_selection(population)
            parent2 = self._tournament_selection(population)
            
            # Crossover
            if random.random() < self.crossover_rate:
                child_prompt = self._crossover(
                    parent1.prompt,
                    parent2.prompt,
                    task_analysis
                )
            else:
                child_prompt = parent1.prompt
            
            # Mutation
            if random.random() < self.mutation_rate:
                child_prompt = self._mutate(child_prompt, task_analysis)
            
            next_gen.append(Individual(
                child_prompt,
                generation=population[0].generation + 1
            ))
        
        return next_gen
    
    def _tournament_selection(
        self,
        population: List[Individual],
        tournament_size: int = 3
    ) -> Individual:
        """Select individual using tournament selection."""
        tournament = random.sample(population, min(tournament_size, len(population)))
        return max(tournament, key=lambda x: x.fitness)
