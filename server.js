import express from 'express';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const PORT = 3000;

// Serve static files from ui folder
app.use(express.static('ui'));

// API endpoint to get emails from Needs_Action folder
app.get('/api/emails', (req, res) => {
    const needsActionPath = path.join(__dirname, 'Needs_Action');
    
    console.log('📂 Reading from:', needsActionPath);
    
    try {
        const files = fs.readdirSync(needsActionPath)
            .filter(file => file.endsWith('.md') && file !== '.gitkeep');
        
        console.log('📧 Found files:', files.length);
        
        const emails = files.map(filename => {
            const filePath = path.join(needsActionPath, filename);
            const content = fs.readFileSync(filePath, 'utf-8');
            
            // Parse frontmatter - handle Windows line endings
            const frontmatterMatch = content.match(/^---[\r\n]+([\s\S]*?)[\r\n]+---/);
            const metadata = {};
            
            if (frontmatterMatch) {
                const frontmatter = frontmatterMatch[1];
                // Split by any line ending (\n or \r\n)
                frontmatter.split(/\r?\n/).forEach(line => {
                    // Handle both quoted and unquoted values
                    const match = line.match(/^(\w+):\s*(.+)$/);
                    if (match) {
                        let value = match[2].trim();
                        // Remove quotes if present
                        if (value.startsWith('"') && value.endsWith('"')) {
                            value = value.slice(1, -1);
                        }
                        metadata[match[1]] = value;
                    }
                });
            }
            
            // Extract preview text (first 200 chars after frontmatter)
            const bodyMatch = content.match(/---[\r\n]+[\r\n]+([\s\S]*)/);
            let preview = '';
            if (bodyMatch) {
                const body = bodyMatch[1]
                    .replace(/^#+\s+.*$/gm, '') // Remove headers
                    .replace(/\*\*.*?\*\*/g, '') // Remove bold
                    .replace(/\[.*?\]\(.*?\)/g, '') // Remove links
                    .replace(/!\[.*?\]\(.*?\)/g, '') // Remove images
                    .replace(/[\r\n]+/g, ' ') // Replace all line endings with spaces
                    .replace(/\s+/g, ' ') // Collapse multiple spaces
                    .trim();
                preview = body.substring(0, 200) + (body.length > 200 ? '...' : '');
            }
            
            // If no preview, use a default message
            if (!preview || preview.length < 10) {
                preview = 'Click to view email details';
            }
            
            return {
                filename,
                subject: metadata.subject || 'No Subject',
                sender: metadata.sender_name || metadata.sender || 'Unknown',
                date: metadata.date || metadata.processed_at || new Date().toISOString(),
                priority: metadata.priority || 'low',
                preview: preview || 'No preview available'
            };
        });
        
        // Sort by date (newest first)
        emails.sort((a, b) => new Date(b.date) - new Date(a.date));
        
        console.log('✅ Sending', emails.length, 'emails');
        res.json(emails);
    } catch (error) {
        console.error('❌ Error reading emails:', error);
        res.status(500).json({ error: 'Failed to load emails', details: error.message });
    }
});

// Start server
app.listen(PORT, () => {
    console.log(`🚀 Dashboard server running at http://localhost:${PORT}`);
    console.log(`📧 Monitoring: ${path.join(__dirname, 'Needs_Action')}`);
    console.log(`\n✨ Open your browser and visit: http://localhost:${PORT}\n`);
});
