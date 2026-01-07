"""
Kevin AI - Agent Prompt Integration Test
Verify all agents are using enhanced prompts

Version: 5.0
Date: January 7, 2026
"""

import sys
print("Testing Kevin AI Agent Prompts Integration...\n")

# Test 1: Import prompts
print("✓ TEST 1: Import Enhanced Prompts")
print("-" * 60)
try:
    from prompts import (
        SOP_ANALYSIS_SYSTEM_PROMPT,
        PROCESS_MAPPING_SYSTEM_PROMPT,
        AUTOMATION_OPPORTUNITY_SYSTEM_PROMPT,
        FUTURE_STATE_DESIGN_SYSTEM_PROMPT,
        TEST_CASE_GENERATOR_SYSTEM_PROMPT,
        CODE_GENERATOR_SYSTEM_PROMPT,
        KPI_CALCULATOR_SYSTEM_PROMPT
    )
    print("✅ All 7 prompts imported successfully")
    print(f"   - SOP Analysis: {len(SOP_ANALYSIS_SYSTEM_PROMPT)} chars")
    print(f"   - Process Mapping: {len(PROCESS_MAPPING_SYSTEM_PROMPT)} chars")
    print(f"   - Automation: {len(AUTOMATION_OPPORTUNITY_SYSTEM_PROMPT)} chars")
    print(f"   - Future State: {len(FUTURE_STATE_DESIGN_SYSTEM_PROMPT)} chars")
    print(f"   - Test Cases: {len(TEST_CASE_GENERATOR_SYSTEM_PROMPT)} chars")
    print(f"   - Code Gen: {len(CODE_GENERATOR_SYSTEM_PROMPT)} chars")
    print(f"   - KPI Calc: {len(KPI_CALCULATOR_SYSTEM_PROMPT)} chars")
except Exception as e:
    print(f"❌ Import failed: {e}")
    sys.exit(1)

print()

# Test 2: Import agents
print("✓ TEST 2: Import Agent Classes")
print("-" * 60)
try:
    from kevin_agents import (
        SOPAnalysisAgent,
        ProcessMappingAgent,
        AutomationOpportunityAgent,
        FutureStateDesignAgent,
        TestCaseGeneratorAgent,
        CodeGeneratorAgent,
        KPICalculatorAgent
    )
    print("✅ All 7 agent classes imported successfully")
except Exception as e:
    print(f"❌ Agent import failed: {e}")
    sys.exit(1)

print()

# Test 3: Check prompt integration
print("✓ TEST 3: Verify Agents Use Enhanced Prompts")
print("-" * 60)

import inspect

def check_agent_uses_prompt(agent_class, prompt_name):
    """Check if agent method uses the specified prompt"""
    # Get the source code of the agent class
    source = inspect.getsource(agent_class)
    return prompt_name in source

agents_to_check = [
    (SOPAnalysisAgent, "SOP_ANALYSIS_SYSTEM_PROMPT", "analyze"),
    (ProcessMappingAgent, "PROCESS_MAPPING_SYSTEM_PROMPT", "map_process"),
    (AutomationOpportunityAgent, "AUTOMATION_OPPORTUNITY_SYSTEM_PROMPT", "identify_opportunities"),
    (FutureStateDesignAgent, "FUTURE_STATE_DESIGN_SYSTEM_PROMPT", "design_future_state"),
    (TestCaseGeneratorAgent, "TEST_CASE_GENERATOR_SYSTEM_PROMPT", "generate_test_cases"),
    (CodeGeneratorAgent, "CODE_GENERATOR_SYSTEM_PROMPT", "generate_code"),
    (KPICalculatorAgent, "KPI_CALCULATOR_SYSTEM_PROMPT", "calculate_kpis")
]

all_connected = True
for agent_class, prompt_name, method_name in agents_to_check:
    uses_prompt = check_agent_uses_prompt(agent_class, prompt_name)
    status = "✅" if uses_prompt else "❌"
    print(f"{status} {agent_class.__name__}.{method_name}() → {prompt_name}")
    if not uses_prompt:
        all_connected = False

print()

if all_connected:
    print("✅ All agents are connected to enhanced prompts!")
else:
    print("⚠️ Some agents still using old inline prompts")

print()

# Test 4: Verify prompt content quality
print("✓ TEST 4: Verify Prompt Quality")
print("-" * 60)

quality_checks = [
    ("SOP Analysis", SOP_ANALYSIS_SYSTEM_PROMPT, 2000, "step-by-step", "JSON"),
    ("Process Mapping", PROCESS_MAPPING_SYSTEM_PROMPT, 1500, "visual_diagram", "swimlanes"),
    ("Automation", AUTOMATION_OPPORTUNITY_SYSTEM_PROMPT, 3000, "ROI", "payback"),
    ("Future State", FUTURE_STATE_DESIGN_SYSTEM_PROMPT, 1500, "optimization", "architecture"),
    ("Test Cases", TEST_CASE_GENERATOR_SYSTEM_PROMPT, 4000, "MINIMUM 30", "pre_conditions"),
    ("Code Generator", CODE_GENERATOR_SYSTEM_PROMPT, 1500, "FastAPI", "production"),
    ("KPI Calculator", KPI_CALCULATOR_SYSTEM_PROMPT, 4000, "financial", "NPV")
]

all_quality_pass = True
for name, prompt, min_length, keyword1, keyword2 in quality_checks:
    length_ok = len(prompt) >= min_length
    has_k1 = keyword1.lower() in prompt.lower()
    has_k2 = keyword2.lower() in prompt.lower()
    
    if length_ok and has_k1 and has_k2:
        print(f"✅ {name:20s} - {len(prompt):5d} chars, comprehensive")
    else:
        print(f"❌ {name:20s} - Issues detected")
        if not length_ok:
            print(f"   ⚠️ Too short: {len(prompt)} < {min_length}")
        if not has_k1:
            print(f"   ⚠️ Missing keyword: {keyword1}")
        if not has_k2:
            print(f"   ⚠️ Missing keyword: {keyword2}")
        all_quality_pass = False

print()

if all_quality_pass:
    print("✅ All prompts meet quality standards!")
else:
    print("⚠️ Some prompts may need enhancement")

print()

# Summary
print("=" * 60)
print("SUMMARY")
print("=" * 60)

if all_connected and all_quality_pass:
    print("🎉 SUCCESS! All agents fully integrated with enhanced prompts")
    print()
    print("✅ All 7 agent classes imported")
    print("✅ All 7 prompts connected")
    print("✅ All prompts meet quality standards")
    print()
    print("Key Improvements:")
    print("  • SOP Analysis: Forensic decomposition framework")
    print("  • Process Mapping: Visual ASCII diagrams (not Mermaid)")
    print("  • Automation: Precise ROI calculations with formulas")
    print("  • Future State: Optimization strategies")
    print("  • Test Cases: Minimum 30 comprehensive tests")
    print("  • Code Generator: Production-ready templates")
    print("  • KPI Calculator: Comprehensive financial analysis")
    print()
    print("🚀 Ready for demo!")
else:
    print("⚠️ Integration partially complete")
    print()
    if not all_connected:
        print("❌ Some agents not using enhanced prompts")
    if not all_quality_pass:
        print("❌ Some prompts need enhancement")
    print()
    print("Review errors above and fix before demo")

print("=" * 60)
