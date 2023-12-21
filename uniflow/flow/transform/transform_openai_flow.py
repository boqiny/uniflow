"""Model Flow Module."""
from typing import Any, Dict, Sequence

from uniflow.constants import TRANSFORM
from uniflow.flow.flow import Flow
from uniflow.flow.transform.model import LLMDataProcessorJson
from uniflow.node.node import Node
from uniflow.op.prompt_schema import GuidedPrompt
from uniflow.op.transform.model_op import LLMDataProcessor, ModelOp


class OpenAIModelFlow(Flow):
    """OpenAI Model Flow Class."""

    def __init__(
        self,
        guided_prompt_template: GuidedPrompt,
        model_config: Dict[str, Any],
    ) -> None:
        """OpenAI Model Flow Constructor.

        Args:
            guided_prompt_template (GuidedPrompt): Guided prompt template.
            model_config (Dict[str, Any]): Model config.
        """
        super().__init__()
        if model_config["response_format"]["type"] == "json_object":
            model = LLMDataProcessorJson(
                guided_prompt_template=guided_prompt_template,
                model_config=model_config,
            )
        else:
            model = LLMDataProcessor(
                guided_prompt_template=guided_prompt_template,
                model_config=model_config,
            )
        self._model_op = ModelOp(
            name="openai_model_op",
            model=model,
        )

    def run(self, nodes: Sequence[Node]) -> Sequence[Node]:
        """Run Model Flow.

        Args:
            nodes (Sequence[Node]): Nodes to run.

        Returns:
            Sequence[Node]: Nodes after running.
        """
        return self._model_op(nodes)


class TransformOpenAIFlow(OpenAIModelFlow):
    TAG = TRANSFORM
