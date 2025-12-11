# Job Report Generator CLI Usage Guide

## Quick Start

Generate a job analysis report with one command:

```bash
python main.py generate-job-report
```

## Command Options

### Basic Usage
```bash
python main.py generate-job-report --language ko --output my_report.pptx
```

### Available Options

| Option | Values | Default | Description |
|--------|--------|---------|-------------|
| `--template` | detailed, summary, executive | detailed | Report template type |
| `--language` | ko, en | ko | Report language (Korean/English) |
| `--output` | filename | job_analysis_report.pptx | Output filename |
| `--db-path` | path | auto-detect | Database path |

## Examples

### Korean Detailed Report
```bash
python main.py generate-job-report --template detailed --language ko
```

### English Summary Report
```bash
python main.py generate-job-report --template summary --language en --output summary_en.pptx
```

### Custom Database Path
```bash
python main.py generate-job-report --db-path ../Job_Management_System/sql_app.db
```

## Output

The command generates a PowerPoint presentation with:
- 조직도 (Organizational Chart)
- FTE 분석 (FTE Analysis)
- RACI 매트릭스 (RACI Matrix)
- 워크로드 대시보드 (Workload Dashboard)
- 등급 분석 (Grade Analysis)

Files are saved to: `output/job_reports/`
