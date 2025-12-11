"use client";

import { GlassCard } from "@/components/ui/glass-card";
import { motion } from "framer-motion";
import { ArrowRight, BarChart2, Users, FileText, Layers } from "lucide-react";

export default function Home() {
  return (
    <main className="min-h-screen p-8 md:p-24 flex flex-col items-center justify-center relative overflow-hidden">
      {/* Background Elements for Depth */}
      <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-purple-500/30 rounded-full blur-[120px] pointer-events-none" />
      <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-blue-500/30 rounded-full blur-[120px] pointer-events-none" />

      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
        className="z-10 text-center mb-16"
      >
        <h1 className="text-5xl md:text-7xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-white to-white/70 mb-6 tracking-tight">
          Job Management System
        </h1>
        <p className="text-xl text-white/60 max-w-2xl mx-auto leading-relaxed">
          Next-Generation HR Intelligence for Public Institutions.
          <br />
          Powered by <span className="text-blue-400 font-semibold">Liquid Glass</span> Design & <span className="text-purple-400 font-semibold">AI Analytics</span>.
        </p>
      </motion.div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 w-full max-w-7xl z-10">
        <GlassCard className="flex flex-col items-center text-center">
          <div className="p-3 rounded-full bg-blue-500/20 mb-4">
            <Users className="w-8 h-8 text-blue-400" />
          </div>
          <h3 className="text-xl font-semibold text-white mb-2">Workforce Planning</h3>
          <p className="text-sm text-white/50">
            Scientific headcount calculation based on productivity analysis.
          </p>
        </GlassCard>

        <GlassCard className="flex flex-col items-center text-center" style={{ transitionDelay: "100ms" }}>
          <div className="p-3 rounded-full bg-purple-500/20 mb-4">
            <Layers className="w-8 h-8 text-purple-400" />
          </div>
          <h3 className="text-xl font-semibold text-white mb-2">Job Classification</h3>
          <p className="text-sm text-white/50">
            NCS-based hierarchy and functional job design.
          </p>
        </GlassCard>

        <GlassCard className="flex flex-col items-center text-center" style={{ transitionDelay: "200ms" }}>
          <div className="p-3 rounded-full bg-pink-500/20 mb-4">
            <FileText className="w-8 h-8 text-pink-400" />
          </div>
          <h3 className="text-xl font-semibold text-white mb-2">Job Description</h3>
          <p className="text-sm text-white/50">
            Dynamic generation linked with recruitment & manuals.
          </p>
        </GlassCard>

        <GlassCard className="flex flex-col items-center text-center" style={{ transitionDelay: "300ms" }}>
          <div className="p-3 rounded-full bg-emerald-500/20 mb-4">
            <BarChart2 className="w-8 h-8 text-emerald-400" />
          </div>
          <h3 className="text-xl font-semibold text-white mb-2">Analytics Dashboard</h3>
          <p className="text-sm text-white/50">
            Real-time insights for every organizational level.
          </p>
        </GlassCard>
      </div>

      <motion.button
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        className="mt-16 px-8 py-4 bg-white/10 hover:bg-white/20 text-white rounded-full font-medium backdrop-blur-md border border-white/20 transition-all flex items-center gap-2 group"
      >
        Enter System <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
      </motion.button>
    </main>
  );
}
