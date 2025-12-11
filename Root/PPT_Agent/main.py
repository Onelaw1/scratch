import argparse
from src.agents.orchestrator import Orchestrator
from src.services.job_report_generator import JobReportGenerator

def main():
    parser = argparse.ArgumentParser(description="Agentic PPT Generator")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Original presentation generation command
    gen_parser = subparsers.add_parser("generate", help="Generate presentation from topic")
    gen_parser.add_argument("topic", type=str, help="The topic of the presentation")
    gen_parser.add_argument("--output", type=str, help="Output filename", default=None)
    
    # Job report generation command
    job_parser = subparsers.add_parser("generate-job-report", help="Generate job analysis report")
    job_parser.add_argument("--template", type=str, choices=["detailed", "summary", "executive"], 
                           default="detailed", help="Report template type")
    job_parser.add_argument("--language", type=str, choices=["ko", "en"], 
                           default="ko", help="Report language")
    job_parser.add_argument("--output", type=str, help="Output filename", 
                           default="job_analysis_report.pptx")
    job_parser.add_argument("--db-path", type=str, help="Path to Job Management System database",
                           default=None)
    
    args = parser.parse_args()
    
    # Handle commands
    if args.command == "generate":
        orchestrator = Orchestrator()
        orchestrator.generate_presentation(args.topic, args.output)
    
    elif args.command == "generate-job-report":
        print(f"Generating job analysis report...")
        print(f"  Template: {args.template}")
        print(f"  Language: {args.language}")
        print(f"  Output: {args.output}")
        
        generator = JobReportGenerator(db_path=args.db_path)
        output_path = generator.generate_full_report(
            filename=args.output,
            language=args.language
        )
        generator.close()
        
        print(f"\n[SUCCESS] Report generated successfully!")
        print(f"File: {output_path}")
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
