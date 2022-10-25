package com.anteifilip.appsec.ui

import android.view.LayoutInflater
import android.view.ViewGroup
import androidx.recyclerview.widget.RecyclerView
import com.anteifilip.appsec.databinding.ViewHolderPostBinding
import com.anteifilip.appsec.models.Post
import com.anteifilip.appsec.utils.onClickDebounced

class PostsAdapter(
    private val posts: List<Post>,
    private val onDeleteClick: (Post) -> Unit
) : RecyclerView.Adapter<PostsAdapter.PostViewHolder>() {

    override fun getItemCount(): Int = posts.count()

    override fun onBindViewHolder(holder: PostViewHolder, position: Int) {
        holder.bind(posts[position])
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int) = PostViewHolder(
        ViewHolderPostBinding.inflate(LayoutInflater.from(parent.context), parent, false)
    )

    inner class PostViewHolder(private val binding: ViewHolderPostBinding) :
        RecyclerView.ViewHolder(binding.root) {

        fun bind(item: Post) {
            binding.apply {
                postTitle.text = item.title
                postContent.text = item.content
                deleteButton.onClickDebounced { onDeleteClick.invoke(item) }
            }
        }
    }
}