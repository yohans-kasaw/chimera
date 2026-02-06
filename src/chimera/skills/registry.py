"""Registry for skill discovery and instantiation."""

from __future__ import annotations

from typing import TypeVar

from pydantic import BaseModel

from chimera.skills.base import Skill

InputT = TypeVar("InputT", bound=BaseModel)
OutputT = TypeVar("OutputT", bound=BaseModel)
SkillType = type[Skill[BaseModel, BaseModel]]


class SkillRegistry:
    """In-memory registry of available skills.

    Args:
        None.

    Returns:
        None.

    Raises:
        None.
    """

    def __init__(self) -> None:
        self._skills: dict[str, SkillType] = {}

    def register(self, skill_cls: type[Skill[InputT, OutputT]]) -> type[Skill[InputT, OutputT]]:
        """Register a skill class by name.

        Args:
            skill_cls: Skill class to register.

        Returns:
            The registered skill class.

        Raises:
            ValueError: If a skill with the same name already exists.
        """
        name = skill_cls.name
        if name in self._skills:
            raise ValueError(f"Skill '{name}' is already registered")
        self._skills[name] = skill_cls
        return skill_cls

    def get(self, name: str) -> SkillType:
        """Fetch a skill class by name.

        Args:
            name: Skill name.

        Returns:
            The skill class.

        Raises:
            KeyError: If the skill does not exist.
        """
        if name not in self._skills:
            raise KeyError(f"Skill '{name}' is not registered")
        return self._skills[name]

    def create(self, name: str) -> Skill[BaseModel, BaseModel]:
        """Instantiate a skill by name.

        Args:
            name: Skill name.

        Returns:
            A skill instance.

        Raises:
            None.
        """
        skill_cls = self.get(name)
        return skill_cls()

    def list_names(self) -> list[str]:
        """List registered skill names.

        Returns:
            Sorted list of skill names.

        Raises:
            None.
        """
        return sorted(self._skills.keys())
