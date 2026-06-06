"""
Queue Tools - AI消息队列工具
支持队列设计、配置生成、优化
"""

import json
import os
from typing import Dict, List, Any
from datetime import datetime

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


class QueueTools:
    """
    AI消息队列工具
    支持：设计、配置、优化
    """

    def __init__(self, model: str = "mimo-v2.5-pro", api_key: str = None, base_url: str = None):
        self.model = model
        if OPENAI_AVAILABLE:
            self.client = OpenAI(
                api_key=api_key or os.environ.get('OPENAI_API_KEY', ''),
                base_url=base_url or os.environ.get('OPENAI_BASE_URL', 'https://api.xiaomimimo.com/v1')
            )
        else:
            self.client = None

    def design_queue_architecture(self, requirements: str) -> Dict:
        """设计队列架构"""
        if not self.client:
            return {"error": "LLM客户端未配置"}

        prompt = f"""请根据以下需求设计消息队列架构：

需求：{requirements}

请返回JSON格式：
{{
    "architecture": "架构描述",
    "components": [
        {{"name": "组件名", "type": "类型", "purpose": "用途"}}
    ],
    "flow": ["消息流程"],
    "tools": ["推荐工具"],
    "scalability": "扩展策略"
}}"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000
        )

        try:
            content = response.choices[0].message.content
            import re
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass

        return {"design": content}

    def generate_rabbitmq_config(self, queues: List[Dict]) -> str:
        """生成RabbitMQ配置"""
        if not self.client:
            return "LLM客户端未配置"

        queues_text = json.dumps(queues, ensure_ascii=False, indent=2)

        prompt = f"""请根据以下队列需求生成RabbitMQ配置：

{queues_text}

请生成完整的配置文件："""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2000
        )

        return response.choices[0].message.content

    def generate_kafka_config(self, topics: List[Dict]) -> str:
        """生成Kafka配置"""
        if not self.client:
            return "LLM客户端未配置"

        topics_text = json.dumps(topics, ensure_ascii=False, indent=2)

        prompt = f"""请根据以下Topic需求生成Kafka配置：

{topics_text}

请生成完整的配置文件："""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2000
        )

        return response.choices[0].message.content

    def optimize_throughput(self, current_config: str, metrics: Dict) -> Dict:
        """优化吞吐量"""
        if not self.client:
            return {"error": "LLM客户端未配置"}

        metrics_text = json.dumps(metrics, ensure_ascii=False)

        prompt = f"""请优化消息队列吞吐量：

当前配置：{current_config}
性能指标：{metrics_text}

请返回JSON格式：
{{
    "bottlenecks": ["瓶颈"],
    "optimizations": [
        {{"parameter": "参数", "current": "当前值", "recommended": "推荐值"}}
    ],
    "expected_improvement": "预期提升"
}}"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )

        try:
            content = response.choices[0].message.content
            import re
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass

        return {"optimization": content}

    def generate_consumer_code(self, queue_type: str, handler: str) -> str:
        """生成消费者代码"""
        if not self.client:
            return "LLM客户端未配置"

        prompt = f"""请生成{queue_type}消费者的Python代码：

处理逻辑：{handler}

要求：
1. 完整可运行
2. 错误处理
3. 重试机制
4. 日志记录"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2000
        )

        return response.choices[0].message.content


def create_tools(**kwargs) -> QueueTools:
    """创建队列工具"""
    return QueueTools(**kwargs)


if __name__ == "__main__":
    tools = create_tools()

    print("Queue Tools")
    print()

    # 测试
    design = tools.design_queue_architecture("电商订单处理，需要异步处理支付、库存、通知")
    print(json.dumps(design, ensure_ascii=False, indent=2))
