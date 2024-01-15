from typing import Any, Generic, TypeVar

from langchain.pydantic_v1 import BaseModel, Field
from langchain_core.messages import BaseMessage

from ..backend.settings import FuncchainSettings, settings

T = TypeVar("T", bound=Any)


class Signature(BaseModel, Generic[T]):
    """
    Fundamental structure of an executable prompt.
    """

    instruction: str
    """ Prompt instruction to the language model. """

    input_args: list[str] = Field(default_factory=list)
    """ List of input arguments for the prompt template. """

    # TODO collect types from input_args
    # -> this would allow special prompt templating based on certain types
    # -> e.g. BaseChatMessageHistory adds a history placeholder
    # -> e.g. BaseChatModel overrides the default language model
    # -> e.g. SettingsOverride overrides the default settings
    # -> e.g. Callbacks adds custom callbacks
    # -> e.g. SystemMessage adds a system message
    # maybe do input_args: list[tuple[str, type]] = Field(default_factory=list)

    output_type: type[T]
    """ Type to parse the output into. """

    # todo: is history really needed? maybe this could be a background optimization
    history: list[BaseMessage] = Field(default_factory=list)
    """ Additional messages that are inserted before the instruction. """

    # update_history: bool = Field(default=True)

    # todo: should this be defined at compile time? maybe runtime is better
    settings: FuncchainSettings = Field(default=settings)
    """ Local settings to override global settings. """

    auto_tune: bool = Field(default=False)
    """ Whether to auto tune the prompt using dspy. """

    class Config:
        arbitrary_types_allowed = True

    def __hash__(self) -> int:
        """Hash for caching keys."""
        return hash(
            (
                self.instruction,
                tuple(self.input_args),
                self.output_type,
                tuple(self.history),
                self.settings,
            )
        )
