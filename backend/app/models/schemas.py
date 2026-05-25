from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

class Trace(Base):
    __tablename__ = "traces"

    id = Column(Integer, primary_key=True, index=True)
    trace_id = Column(String, unique=True, index=True, nullable=False)
    session_id = Column(String, index=True)
    correlation_id = Column(String, index=True)
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime)
    latency = Column(Float)  # In seconds
    total_tokens = Column(Integer, default=0)
    total_cost = Column(Float, default=0.0)
    status = Column(String, index=True)  # e.g., success, failure

    spans = relationship("Span", back_populates="trace")
    evaluations = relationship("Evaluation", back_populates="trace")
    feedback = relationship("FeedbackRecord", back_populates="trace")
    attacks = relationship("AttackResult", back_populates="trace")

class Span(Base):
    __tablename__ = "spans"

    id = Column(Integer, primary_key=True, index=True)
    trace_id = Column(String, ForeignKey("traces.trace_id"), index=True)
    span_id = Column(String, unique=True, index=True, nullable=False)
    parent_span_id = Column(String, index=True)
    name = Column(String, index=True)
    span_type = Column(String, index=True)  # llm, tool, chain, agent
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime)
    attributes = Column(JSON)  # input_messages, output_messages, metadata
    status = Column(String)

    trace = relationship("Trace", back_populates="spans")
    tool_calls = relationship("ToolCall", back_populates="span")

class ToolCall(Base):
    __tablename__ = "tool_calls"

    id = Column(Integer, primary_key=True, index=True)
    span_id = Column(String, ForeignKey("spans.span_id"), index=True)
    tool_name = Column(String, index=True)
    inputs = Column(JSON)
    outputs = Column(JSON)
    error = Column(Text)

    span = relationship("Span", back_populates="tool_calls")

class Evaluation(Base):
    __tablename__ = "evaluations"

    id = Column(Integer, primary_key=True, index=True)
    trace_id = Column(String, ForeignKey("traces.trace_id"), index=True)
    metric_name = Column(String, index=True)
    score = Column(Float)
    reasoning = Column(Text)
    evaluator_model = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    trace = relationship("Trace", back_populates="evaluations")

class PromptVersion(Base):
    __tablename__ = "prompt_versions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    template = Column(Text)
    version_hash = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class ModelVersion(Base):
    __tablename__ = "model_versions"

    id = Column(Integer, primary_key=True, index=True)
    provider = Column(String, index=True)
    model_name = Column(String, index=True)
    parameters = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

class FeedbackRecord(Base):
    __tablename__ = "feedback_records"

    id = Column(Integer, primary_key=True, index=True)
    trace_id = Column(String, ForeignKey("traces.trace_id"), index=True)
    user_id = Column(String, index=True)
    rating = Column(Integer)  # e.g., 1-5
    comment = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    trace = relationship("Trace", back_populates="feedback")

class FailureCluster(Base):
    __tablename__ = "failure_clusters"

    id = Column(Integer, primary_key=True, index=True)
    cluster_name = Column(String, index=True)
    description = Column(Text)
    representative_trace_id = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class Changelog(Base):
    __tablename__ = "changelog"

    id = Column(Integer, primary_key=True, index=True)
    entity_type = Column(String, index=True)  # prompt, model
    entity_id = Column(Integer)
    author = Column(String)
    change_type = Column(String)
    before_value = Column(JSON)
    after_value = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

class AttackResult(Base):
    __tablename__ = "attack_results"

    id = Column(Integer, primary_key=True, index=True)
    trace_id = Column(String, ForeignKey("traces.trace_id"), index=True)
    attack_type = Column(String, index=True)  # jailbreak, injection
    success_flag = Column(Boolean)
    payload = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    trace = relationship("Trace", back_populates="attacks")
