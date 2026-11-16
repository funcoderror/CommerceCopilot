
import json

from src.rag.rag_pipeline import (
    groq_client,
    retrieve_context
)

from src.tools.tools import (
    search_product,
    check_inventory,
    get_order_status,
    get_catalog_summary
)

from src.memory.chat_memory import (
    initialize_database,
    save_message,
    get_history
)


# Initialize chat memory
initialize_database()


# 1. Describe available tools to Groq

tool_definitions = [

    {
    "type": "function",
    "function": {
        "name": "get_catalog_summary",
        "description": (
            "Get the complete product catalog summary, "
            "including total product count, product categories "
            "and brand counts. Use this whenever the user asks "
            "about the overall inventory, total products or "
            "available product categories."
        ),
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
},

    {
        "type": "function",
        "function": {
            "name": "search_knowledge_base",
            "description": (
                "Search company documents for information "
                "about return policies, shipping, refunds, "
                "warranties and customer support."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {
                        "type": "string",
                        "description": "Question to search in company documents."
                    }
                },
                "required": ["question"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "search_product",
            "description": "Search for products using a product name or product ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Product name or product ID to search for."
                    }
                },
                "required": ["query"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "check_inventory",
            "description": "Check the stock quantity and availability of a product.",
            "parameters": {
                "type": "object",
                "properties": {
                    "product_id": {
                        "type": "string",
                        "description": "The product ID."
                    }
                },
                "required": ["product_id"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "get_order_status",
            "description": "Retrieve order status, payment status and delivery information.",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "The customer's order ID."
                    }
                },
                "required": ["order_id"]
            }
        }
    }
]


# 2. Knowledge base function

def search_knowledge_base(question):

    context = retrieve_context(question)

    if not context.strip():
        return {
            "message": "No relevant information found."
        }

    return {
        "retrieved_context": context
    }


# 3. Map tool names to Python functions

available_functions = {
    "search_product": search_product,
    "check_inventory": check_inventory,
    "get_order_status": get_order_status,
    "search_knowledge_base": search_knowledge_base,
    "get_catalog_summary": get_catalog_summary
}


# 4. Main tool-calling function with memory

def run_tool_assistant(user_query):

    # Load previous conversation before adding the new message
    history = get_history(limit=10)

    # Save the current user message
    save_message("user", user_query)

    # System instructions
    system_message = {
        "role": "system",
        "content": """
            You are CommerceCopilot, an AI-powered e-commerce shopping and customer-support assistant.

            DOMAIN RESTRICTION:
            - Only answer questions related to shopping, products, inventory, orders, returns, refunds, shipping and company policies.
            - Politely decline unrelated questions, including general knowledge, sports, politics and entertainment.
            - Never answer unrelated questions using your pretrained knowledge.

            ACCURACY:
            - Never invent product details, prices, stock availability, order status or company policies.
            - Use available tools whenever factual company information or transactional information is requested.
            - Use retrieved documents for company policies and relevant product information.
            - If information is unavailable, clearly tell the user.
            - Never pretend a tool was successfully executed if it failed.

            CONVERSATION:
            - Understand follow-up questions using conversation history.
            - Maintain the context of the current conversation.
            - Do not unnecessarily repeat information already provided.

            AVAILABLE CAPABILITIES:
            1. Product search
            2. Inventory checking
            3. Order status lookup
            4. Company knowledge base retrieval
            5. Catalog summary retrieval

            TOOL INSTRUCTIONS:
            - Use tools whenever factual company information or transactional information is requested.
            - Use search_knowledge_base for company policies and documentation.
            - Use database tools for products, stock and orders.
            - You may call multiple tools when needed.
            - Never invent product, inventory, order or policy data.
            - If information is unavailable, clearly say so.
            - Combine results into one helpful answer.
            - Do not expose raw tool execution details.
            - Use previous conversation messages to understand follow-up questions and references.
            - Use get_catalog_summary whenever users ask about total products, overall inventory or product categories.
            - Use actual catalog data when discussing available products. Never assume products exist based on general knowledge.
            """
    }


    # Combine system message, previous history and current query
    messages = [
        system_message
    ] + history + [
        {
            "role": "user",
            "content": user_query
        }
    ]

    # Allow multiple rounds of tool execution
    max_tool_rounds = 4

    for round_number in range(max_tool_rounds):

        response = groq_client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=messages,
            tools=tool_definitions,
            tool_choice="auto",
            max_completion_tokens=700
        )

        response_message = response.choices[0].message

        # If no more tools are needed
        if not response_message.tool_calls:

            final_answer = response_message.content or ""

            # Save assistant response in memory
            save_message("assistant", final_answer)

            return final_answer

        # Add assistant tool request to conversation
        messages.append(
            response_message.model_dump(exclude_none=True)
        )

        # Execute requested tools
        for tool_call in response_message.tool_calls:

            function_name = tool_call.function.name

            function_args = json.loads(
                tool_call.function.arguments
            )

            function_to_call = available_functions.get(
                function_name
            )

            if function_to_call is None:

                function_result = {
                    "error": "Requested tool is unavailable."
                }

            else:

                try:

                    function_result = function_to_call(
                        **function_args
                    )

                except Exception as e:

                    function_result = {
                        "error": str(e)
                    }

            # Send tool result back to Groq
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(
                    function_result,
                    default=str
                )
            })

    # Force a final response after tool-call limit
    final_response = groq_client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=messages,
        tool_choice="none",
        max_completion_tokens=700
    )

    final_answer = final_response.choices[0].message.content or ""

    # Save final assistant response
    save_message("assistant", final_answer)

    return final_answer
